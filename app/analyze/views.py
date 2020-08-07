from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AnalyzeSerializer


def characters_count(string):
    """Count only the characters (not numbers)
    occurrences in the string"""
    result = []
    sorted_string_without_space = sorted(string)
    modified_string = ''.join([i for i in sorted_string_without_space
                               if not i.isdigit()])
    unique_characters = set()
    if modified_string:
        for c in modified_string:
            if c not in unique_characters:
                unique_characters.add(c)
                result.append({c: modified_string.count(c)})
    return result


@api_view(['POST'])
def analyze_data(request):
    serializer = AnalyzeSerializer(data=request.data)
    if serializer.is_valid():
        payload = serializer.data['text']
        with_space = len(payload)
        with_out_space = "".join(payload.split()).lower()

        result = {
            "textLength": {
                "withSpaces": with_space,
                "withoutSpaces": len(with_out_space),
            },
            "wordCount": len(payload.split()),
            "characterCount": characters_count(with_out_space),
        }
        return Response(result, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
