from django.contrib import admin
from dtc.models import DTCData


class DTCDataAdmin(admin.ModelAdmin):
    search_fields = ['meter_serial_number', 'mpan']

    list_display = (
    'record_id', 'mpan', 'meter_serial_number', 'meter_reading', 'imported_file_name', 'file_imported_at')


admin.site.register(DTCData, DTCDataAdmin)
