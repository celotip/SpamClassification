from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from spam_detection.service import Spam

spam_detector = Spam.worker()

@api_view(['POST'])
def api_predict_spam(request):
    text = request.data.get('text')
    if not text:
        return Response({'error': 'Text is required.'}, status=status.HTTP_400_BAD_REQUEST)

    is_spam, reasons = spam_detector.predict(text)
    return Response({
        'is_spam': is_spam,
        'reasons': reasons
    })


@api_view(['GET'])
def api_evaluate_accuracy(request):
    accuracy = Spam.evaluate()
    return Response({'accuracy': round(accuracy, 2)})


@api_view(['POST'])
def api_report_spam(request):
    text = request.data.get('text')
    if not text:
        return Response({'error': 'Text is required.'}, status=400)

    # Marked as spam by user
    Spam.retrain_with_reported_data([(text, 1)])  # 1 means spam
    return Response({'message': 'Reported and retrained'}, status=200)
