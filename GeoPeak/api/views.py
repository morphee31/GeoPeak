import csv
from io import StringIO

from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from .models import Peak
from .serializers import PeakSerialiser


class ListPeakViews(APIView):
    """
    CRUD Api from peak
    """

    def get(self, request, *args, **kwargs):
        """List all peak record"""
        peak_name = request.GET.get("name", None)
        if peak_name:
            peaks = Peak.objects.filter(name__icontains=peak_name)
        else:
            peaks = Peak.objects.all()

        peak_serialiser = PeakSerialiser(peaks, many=True)
        return JsonResponse(peak_serialiser.data, safe=False)

    def post(self, request, *args, **kwargs):
        """
            create peak record.
            Pass json body
                {
                    "name": "Mont",
                    "lat": 42.6755556,
                    "long": 0.03444444,
                    "altitude": 3348
                }
        """
        new_peak_data = JSONParser().parse(request)
        new_peak_serialiser = PeakSerialiser(data=new_peak_data)
        if new_peak_serialiser.is_valid():
            new_peak_serialiser.save()
            json_response = JsonResponse(new_peak_serialiser.data, status=status.HTTP_201_CREATED)
        else:
            json_response = JsonResponse(new_peak_serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
        return json_response


class DetailPeakViews(APIView):
    """CRUD Api from peak
     get:
        Retunrn list
    """

    def get(self, request, *args, **kwargs):
        """
        Get peak by id.
        """
        try:
            peak = Peak.objects.get(pk=kwargs["pk"])
            peak_serialiser = PeakSerialiser(peak, many=False)
            json_response = JsonResponse(peak_serialiser.data, safe=False)
        except Peak.DoesNotExist:
            json_response = JsonResponse({'message': 'The peak does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return json_response

    def put(self, request, *args, **kwargs):
        """
        Update peak record by id.
        Pass json body
            {
                "name": "Mont",
                "lat": 42.6755556,
                "long": 0.03444444,
                "altitude": 3348
            }
        """
        try:
            peak = Peak.objects.get(pk=kwargs["pk"])
            data_to_update = JSONParser().parse(request)
            updated_peak_serialiser = PeakSerialiser(peak, data=data_to_update)
            if updated_peak_serialiser.is_valid():
                updated_peak_serialiser.save()
                json_response = JsonResponse(updated_peak_serialiser.data)
            else:
                json_response = JsonResponse(updated_peak_serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
        except Peak.DoesNotExist:
            json_response = JsonResponse({'message': 'The peak does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return json_response

    def delete(self, request, *args, **kwargs):
        """
        Remove peak record by id
        """
        try:
            peak = Peak.objects.get(pk=kwargs["pk"])
            peak.delete()
            json_response = JsonResponse({'message': 'Peak was deleted successfully!'},
                                         status=status.HTTP_200_OK)
        except Peak.DoesNotExist:
            json_response = JsonResponse({'message': 'The peak does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return json_response


@api_view(["POST"])
def upload_list_peak(request):
    """
    Record peaks from csv file
    (csv format : name|altitude|latitude|longitude)
    """
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
