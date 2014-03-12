"""
Classes for verifying and capturing LTI information
"""

from collections import OrderedDict
import urllib
from django.http import Http404
from oauthlib.oauth1.rfc5849 import signature
from models import Consumer
from grapher.middleware.http import Http403


class Lti():
    """
    Class for verifying OAuth from LTI and setting session cookies for user_id and role for later requests
    """
    __httprequest = None

    def __init__(self, request, required):
        self.__httprequest = request
        self.setsession(required)

    def setsession(self, required):
        """
        Checks for a new LTI session (LTI POST) and sets session cookies based on success
        :param required: (Boolean) whether LTI is required to continue
        """
        if self.__httprequest.POST:
            postdata = dict(self.__httprequest.POST.dict())
            #check if its LTI call
            if postdata.get("lti_message_type") == "basic-lti-launch-request":
                if self.check_oauth():
                    print postdata
                    self.__httprequest.session["lti_validsession"] = True
                    self.__httprequest.session["lti_user_id"] = postdata.get("user_id")
                    self.__httprequest.session["lti_role"] = postdata.get("roles")
                    print "NEW LTI SESSION"
                    raise Http403
                else:
                    print "GENERATING 404 - BAD OAUTH DATA"
                    raise Http404
        elif self.is_valid() is not True and required:
            raise Http403("NOT AN LTI CALL AND LTI IS REQUIRED")

    def is_valid(self):
        """
        Checks whether the LTI session variables have been stored
        :return: user_id
        """
        if "lti_validsession" not in self.__httprequest.session:
            return False
        return True

    def get_userid(self):
        """
        Returns the user ID from the LTI request
        :return: user_id
        """
        user_id = ""
        if self.is_valid():
            user_id = self.__httprequest.session["lti_user_id"]
        return user_id

    def check_oauth(self):
        """
        Checks whether the request passes Oauth signature check
        :return valid_oauth
        """
        resp = dict(self.__httprequest.POST.dict())
        orderedresp = OrderedDict(sorted(resp.items(), key=lambda t: t[0]))
        query_string = urllib.urlencode(orderedresp)
        oauth_headers = dict(signature.collect_parameters(query_string, exclude_oauth_signature=False))
        sig = oauth_headers.pop('oauth_signature')
        consumer_secret = self.get_oauthsecret_for_key(orderedresp.get('oauth_consumer_key'))

        oauthrequest = Oauthrequest()
        oauthrequest.params = oauth_headers.items()
        oauthrequest.uri = unicode(urllib.unquote(self.__httprequest.build_absolute_uri()))
        oauthrequest.http_method = unicode('POST')
        oauthrequest.signature = sig
        if signature.verify_hmac_sha1(request=oauthrequest, client_secret=unicode(consumer_secret)):
            return True
        return False

    @staticmethod
    def get_oauthsecret_for_key(consumer_key):
        """
        Retuns a the oauth consumer secret based on the consumer key
        :param consumer_key: the consumer key
        :return consumer_secret
        """
        return Consumer.getsecretforkey(consumer_key)


class Oauthrequest():
    """
    A mock object to pass to the OAuth library
    """

    def __init__(self):
        self.uri = unicode("")
        self.http_method = unicode("")
        self.params = unicode("")
        self.signature = unicode("")