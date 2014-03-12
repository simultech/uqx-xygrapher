"""
XYGrapher Views
"""
import random
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.views.decorators.clickjacking import xframe_options_exempt
import json
from models import *
from lti import *
from django.conf import settings
from django.views.decorators.cache import never_cache


@xframe_options_exempt
@csrf_exempt
@ensure_csrf_cookie
def index(request):
    """
    :param request:
    :return:
    """
    lti = Lti(request, True)
    student_id = lti.get_userid()
    template = loader.get_template('index.html')
    contextvars = {
        'student_id': student_id
    }
    contextvars = lti.setvariables(request, contextvars, {
        'multiple_attempts': settings.XYGRAPHER_MULTIPLE_ATTEMPTS,
        'require_grade': settings.XYGRAPHER_REQUIRES_GRADE,
        'submit_button': settings.XYGRAPHER_SUBMIT_BUTTON,
        'x_axis_label': settings.XYGRAPHER_CONFIG_XAXIS,
        'y_axis_label': settings.XYGRAPHER_CONFIG_YAXIS,
        'min_x_value': settings.XYGRAPHER_MIN_X_VALUE,
        'min_y_value': settings.XYGRAPHER_MIN_Y_VALUE,
        'max_x_value': settings.XYGRAPHER_MAX_X_VALUE,
        'max_y_value': settings.XYGRAPHER_MAX_Y_VALUE,
        'showlines': settings.XYGRAPHER_SHOWLINES,
    })
    if lti.is_valid():
       contextvars['post'] = lti.get_userid()
    print contextvars
    context = RequestContext(request, contextvars)
    response = HttpResponse(template.render(context))
    response['P3P'] = 'CP="We do not have a P3P policy."'
    return response

@never_cache
def data(request):
    """
    Gets the data list of other points
    :param request:
    :return:
    """
    response_data = {}
    lti = Lti(request, False)
    if lti.is_valid():
        student_id = lti.get_userid()
        response_data['data'] = Plotpoint.getall()
        mycoord = Plotpoint.objects(uid=student_id).first()
        if mycoord:
            response_data['entered'] = 'true'
            response_data['current_x'] = mycoord.x
            response_data['current_y'] = mycoord.y
            response_data['data'].append({"x": mycoord.x, "y": mycoord.y, "user": "true"})
        else:
            response_data['entered'] = 'false'
    else:
        response_data['entered'] = 'false'
        response_data['data'] = []
    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['P3P'] = 'CP="We do not have a P3P policy."'
    return response


@csrf_exempt
@require_http_methods(["POST"])
def savecoord(request):
    """
    Saves the new users coordinate into the mongo collection
    :param request:
    :return:whether it was saved
    """
    lti = Lti(request, True)
    student_id = lti.get_userid()
    response_data = {'saved': 'false'}
    if student_id != "":
        x_pos = float(request.POST.get('x', 0.0))
        y_pos = float(request.POST.get('y', 0.0))
        Plotpoint.saveorupdate(dict(uid=student_id, x=x_pos, y=y_pos), settings.XYGRAPHER_MULTIPLE_ATTEMPTS)
        response_data = {'saved': 'true'}
    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['P3P'] = 'CP="We do not have a P3P policy."'
    return response


# noinspection PyUnusedLocal
def generate(request):
    """

    :param request:
    :return:
    """
    use_curve = True
    percentage_incorrect = 10
    x_shift = -3
    x_start = 5
    x_end = 15
    x_increment = 0.01
    x = x_start
    while x < x_end:
        x += x_increment
        user_id = 's40000_'+str(x)
        if use_curve:
            zx = x+x_shift
            a = 0.1
            b = -1
            c = -0.1
            d = 25
            offset = 0
            if random.randint(0, 100) < percentage_incorrect:
                offset = random.randint(0, 20)-10
            y_val = a*(zx*zx*zx) + b*(zx*zx) + c*zx + d + offset
        else:
            y_val = random.randint(0, 1000)
        item = dict(uid=user_id, x=x, y=y_val)
        Plotpoint.saveorupdate(item)
    response_data = {'generated': 'truez'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")