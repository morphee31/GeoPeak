import csv
from io import StringIO

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from .models import Peak
from .serializers import PeakSerialiser


@csrf_exempt
@api_view(["GET", "POST"])
def list_peak(request):
    if request.method == "GET":
        peak_name = request.GET.get("name", None)
        if peak_name:
            peaks = Peak.objects.filter(name__icontains=peak_name)
        else:
            peaks = Peak.objects.all()

        peak_serialiser = PeakSerialiser(peaks, many=True)
        json_response = JsonResponse(peak_serialiser.data, safe=False)
    elif request.method == "POST":
        new_peak_data = JSONParser().parse(request)
        new_peak_serialiser = PeakSerialiser(data=new_peak_data)
        if new_peak_serialiser.is_valid():
            new_peak_serialiser.save()
            json_response = JsonResponse(new_peak_serialiser.data, status=status.HTTP_201_CREATED)
        else:
            json_response = JsonResponse(new_peak_serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        count = Peak.objects.all().delete()
        json_response = JsonResponse({'message': f'{count} peaks was deleted successfully!'},
                                     status=status.HTTP_204_NO_CONTENT)

    return json_response


@api_view(["GET", "PUT", "DELETE"])
def detail_peak(request, pk):
    """
    Read a record
    :param request:
    :return:
    """

    try:
        peak = Peak.objects.get(pk=pk)
    except Peak.DoesNotExist:
        return JsonResponse({'message': 'The peak does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        peak_serialiser = PeakSerialiser(peak, many=False)
        json_response = JsonResponse(peak_serialiser.data, safe=False)
    elif request.method == "PUT":
        data_to_update = JSONParser().parse(request)
        updated_peak_serialiser = PeakSerialiser(peak, data=data_to_update)
        if updated_peak_serialiser.is_valid():
            updated_peak_serialiser.save()
            json_response = JsonResponse(updated_peak_serialiser.data)
        else:
            json_response = JsonResponse(updated_peak_serialiser.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        peak.delete()
        json_response = JsonResponse({'message': 'Peak was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    return json_response


@api_view(["POST"])
def upload_list_peak(request):
    uploaded_file = request.FILES["file"]
    json_response = []
    for chunk in uploaded_file.chunks():
        iofile = StringIO(chunk.decode("utf8"))
        uploaded_csv = csv.reader(iofile, delimiter="|")
        for item in uploaded_csv:
            peak_data = {
                "name": item[0],
                "altitude": item[1],
                "lat": item[2],
                "long": item[3]
            }
            peaks_serialiser = PeakSerialiser(data=peak_data)
            if peaks_serialiser.is_valid():
                peaks_serialiser.save()
                peak_data["record_status"] = "success"
            else:
                peak_data["record_status"] = "error"
            json_response.append(peak_data)
    return JsonResponse(json_response, safe=False)
