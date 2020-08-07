from rest_framework import serializers
from django.core.exceptions import ValidationError


class AnalyzeSerializer(serializers.Serializer):
    """Serializer for Analyze API payload object"""
    text = serializers.CharField(trim_whitespace=False, max_length=200)

    def validate_text(self, value):
        """
        Check that the text value is string only
        """
        # print(type(value))
        if not isinstance(value, str):
            raise serializers.ValidationError("'text' value should be string")
        return str(value)

    def validate(self, attrs):
        unknown = set(self.initial_data) - set(self.fields)
        unknown = sorted(unknown)
        if unknown:
            raise ValidationError("Unknown field(s): {}"
                                  .format(", ".join(unknown)))
        return attrs
