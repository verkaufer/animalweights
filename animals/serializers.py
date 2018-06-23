from rest_framework import serializers

from animals.models import Animal, Weight


class AnimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        exclude = ('id',)


class WeightSerializer(serializers.Serializer):
    """
    Serialize and record a new weight record
    """
    weight = serializers.FloatField()
    weigh_date = serializers.DateTimeField()

    def save(self, animal):

        return Weight.objects.create(
            animal_id=animal.id,
            recorded_weight=self.validated_data['weight'],
            recorded_at=self.validated_data['weigh_date']
        )
