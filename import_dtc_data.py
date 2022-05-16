########################################################################################
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()
########################################################################################


import sys
import os
from dtc.models import DTCData


def extract_data_from_electric_file(all_electric_data_lines):
    formatted_electric_data = []

    valid_start_lines = ['026', '028', '030']

    current_electric_data = {}
    for data_line in all_electric_data_lines:
        # split the data at "pipe" delimiter
        electric_data = data_line.split('|')

        # if there is no data, continue for the next
        if not electric_data or len(electric_data) < 2:
            continue

        # we do not need any data lines that does not give mpan, meter reading or reading values
        if electric_data[0] not in valid_start_lines:
            continue

        """
            If a line starts from 026, MPAN will be the number coming after the first "pipe" delimiter.
            If a line starts from 028, Meter serial number will be the number coming after the first "pipe" delimiter.
            If a line starts from 030, Meter reading will be the number coming after the third "pipe" delimiter. 
        """
        if electric_data[0] == '026':
            current_electric_data['mpan'] = electric_data[1]

        if electric_data[0] == '028':
            current_electric_data['meter_serial_number'] = electric_data[1]

        if electric_data[0] == '030':
            current_electric_data['meter_reading_number'] = electric_data[3]
            formatted_electric_data.append(current_electric_data)
            current_electric_data = {}

    return formatted_electric_data


def read_the_file(file_name):
    # Take args from the command line and check if it is a valid file name or not.
    if not os.path.exists(file_name):
        print('Invalid filename. Specify valid DTO file name with complete absolute path.')
        return

    f = open(file_name, 'r')
    file_contents = f.read()
    if not file_contents:
        print('No content found in the file')
        return

    all_electric_data_lines = file_contents.split('\n')
    return all_electric_data_lines


def import_data_into_db(formatted_electric_data, file_path):
    file_name = os.path.basename(file_path)

    for ele_data in formatted_electric_data:
        mpan = ele_data.get('mpan', None)
        meter_serial_number = ele_data.get('meter_serial_number', None)
        meter_reading_number = ele_data.get('meter_reading_number', None)

        # if there is no data present, do not insert into db, continue for next record
        if not mpan or not meter_serial_number or not meter_reading_number:
            continue

        DTCData.objects.create(mpan=mpan, meter_serial_number=meter_serial_number,
                               meter_reading=meter_reading_number, imported_file_name=file_name)


if __name__ == '__main__':
    no_of_args = len(sys.argv)
    if no_of_args < 2:
        print('Please specify the DTO file name to import.')
        exit()

    if no_of_args > 2:
        print('Invalid filename. Please specify only DTO file name.')
        exit()

    try:
        file_name = sys.argv[1]
        print(file_name)

        all_electric_data_lines = read_the_file(file_name)
        formatted_electric_data = extract_data_from_electric_file(all_electric_data_lines)
        import_data_into_db(formatted_electric_data, file_name)
    except Exception as e:
        print(str(e))
        print('Something went wrong. Please try again')
        exit()
