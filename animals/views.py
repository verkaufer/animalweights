from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import scipy.interpolate

from animals.models import Animal, Weight
from animals.serializers import AnimalSerializer, WeightSerializer
from animals.utils import transform_to_unixtime


class AnimalListView(ListCreateAPIView):

    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


class AnimalDetailView(RetrieveAPIView):

    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


class RecordWeightView(CreateAPIView):
    serializer_class = WeightSerializer

    def perform_create(self, serializer):
        animal = get_object_or_404(Animal, pk=self.kwargs.get('pk'))
        return serializer.save(animal=animal)


class EstimatedWeightView(APIView):

    def get(self, request, *args, **kwargs):

        # Check for a date query_params. Considered a required field for sake of time.
        if 'date' not in self.request.query_params:
            return Response({"error": {"Missing timestamp for request."}},
                            status=status.HTTP_400_BAD_REQUEST)

        # Parse the date from URL into a convertable datetime format.
        try:
            parsed_request_date = datetime.strptime(
                self.request.query_params.get('date'),
                '%Y-%m-%dT%H:%M:%SZ'
            )
            requested_date = transform_to_unixtime(parsed_request_date.timetuple())
        except ValueError:
            return Response({"error": {"Invalid timestamp format."}},
                            status=status.HTTP_400_BAD_REQUEST)

        # Lookup the weights for our animal, auto-order into ascending by datetime
        animal = get_object_or_404(Animal, pk=self.kwargs.get('pk'))
        weights = Weight.objects.filter(animal=animal).order_by('recorded_at').all()

        if not weights:
            return Response({"estimated_weight": None})

        recorded_weight = []
        timestamps = []

        # Split queryset results into 2 lists for the interp1d function
        for weigh_record in weights:
            recorded_weight.append(weigh_record.recorded_weight)
            timestamps.append(
                transform_to_unixtime(weigh_record.recorded_at)
            )

        # Utilize scipy's interpolate function
        # Speed considerations: https://stackoverflow.com/a/33333070
        # Scipy also allows for `fill_value` to do extrapolation if requested_date is
        # outside range
        interpolated_weight = scipy.interpolate.interp1d(timestamps,
                                                         recorded_weight,
                                                         fill_value="extrapolate")
        return Response({'estimated_weight': interpolated_weight(requested_date)})
