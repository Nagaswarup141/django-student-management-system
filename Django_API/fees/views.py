from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import FeeRecord
from .serializers import FeeRecordSerializer, RecordPaymentSerializer

class FeeListCreateView(generics.ListCreateAPIView):
    queryset           = FeeRecord.objects.select_related('student','course')
    serializer_class   = FeeRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['student__first_name','student__last_name','student__student_id']

    def get_queryset(self):
        qs         = super().get_queryset()
        student_id = self.request.query_params.get('student')
        semester   = self.request.query_params.get('semester')
        if student_id: qs = qs.filter(student_id=student_id)
        if semester:   qs = qs.filter(semester=semester)
        return qs

class FeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset           = FeeRecord.objects.all()
    serializer_class   = FeeRecordSerializer
    permission_classes = [IsAuthenticated]

class RecordPaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        fee = FeeRecord.objects.get(pk=pk)
        ser = RecordPaymentSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        amount = min(ser.validated_data['amount'], fee.outstanding)
        fee.paid_amount  += amount
        fee.payment_mode  = ser.validated_data['payment_mode']
        fee.save()
        return Response({'message':'Payment recorded.','paid':float(fee.paid_amount),'outstanding':fee.outstanding,'status':fee.status})

class FeeStatsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        agg = FeeRecord.objects.aggregate(total_billed=Sum('total_amount'), total_paid=Sum('paid_amount'))
        billed = float(agg['total_billed'] or 0)
        paid   = float(agg['total_paid']   or 0)
        outstanding = billed - paid
        rate = round((paid/billed*100),1) if billed else 0
        return Response({'total_billed':billed,'total_collected':paid,'total_outstanding':outstanding,'collection_rate':rate,
            'pending_count':FeeRecord.objects.filter(paid_amount=0).count()})
