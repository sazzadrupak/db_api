from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AnalyzeSerializer


def characters_count(sorted_string):
    """Count only the characters (not numbers)
    occurrences in the string"""
    result = []
    if sorted_string:
        unique_characters = set(sorted_string)
        unique_characters = sorted(unique_characters)
        for c in unique_characters:
            result.append({c: sorted_string.count(c)})
    return result


@api_view(['POST'])
def analyze_data(request):
    serializer = AnalyzeSerializer(data=request.data)
    if serializer.is_valid():
        payload = serializer.data['text']
        with_space_len = len(payload)
        with_out_space = "".join(payload.split()).lower()
        only_characters = ''.join(filter(str.isalpha, with_out_space))

        result = {
            "textLength": {
                "withSpaces": with_space_len,
                "withoutSpaces": len(with_out_space),
            },
            "wordCount": len(payload.split()),
            "characterCount": characters_count(only_characters),
        }
        return Response(result, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
