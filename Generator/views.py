from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import os
import docx
import json
import codecs
from docx.shared import RGBColor, Inches, Pt
from django.http import HttpResponse
from django.conf import settings
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Skill, Level

@csrf_exempt
def index(request):
    if request.method == "POST":
        sk1 = request.POST['sk1']
        sk1_start = int(request.POST['sk1_min'])
        sk1_stop = int(request.POST['sk1_max'])
        sk2 = request.POST['sk2']
        sk2_start = int(request.POST['sk2_min'])
        sk2_stop = int(request.POST['sk2_max'])
        type = request.POST['type']
        if is_valid(request,type,sk1,sk2,sk1_start,sk2_start,sk1_stop,sk2_stop):
            return generate(request,type,sk1,sk2,sk1_start,sk2_start,sk1_stop,sk2_stop)
        else:
            template = loader.get_template('invalid.html')
            context = {}
            return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('form.html')
        context = {}
        return HttpResponse(template.render(context, request))

def is_valid(request,type,sk1,sk2,sk1_start,sk2_start,sk1_stop,sk2_stop):
    if sk1_start>=1 and sk2_start>=1 and sk1_stop<=7 and sk2_stop<=7 and (type=='student' or type=='employer'):
        try:
            skill_object = Skill.objects.get(code=sk1.lower())
        except: return False
        try:
            skill_object = Skill.objects.get(code=sk2.lower())
        except:
            return False
        return True
    else: return False

def generate(request,type,sk1,sk2,sk1_start,sk2_start,sk1_stop,sk2_stop):

    def get_skill(sk_code):

        skill_object = Skill.objects.get(code=sk_code.lower())

        skill = {
            'name':skill_object.name,
            'code':skill_object.code,
            'description':skill_object.description,
            'levels':[]
        }
        for level in Level.objects.filter(skill = skill_object):
            skill['levels'].append({
                'level':level.level,
                'description':level.description,
            })
        return skill

    def get_levels(sk_code, sk_range):

        sk = get_skill(sk_code)
        levels = []

        for i in range(sk_range[0], sk_range[1] + 1):
            for level in sk['levels']:
                if level['level'] == i:
                    description = level['description']
                    levels.append({'level': i, 'description': description})
                    break
        return levels

    def add_skill_table(sk_code, sk_range):

        # Get the information for the skill
        levels = get_levels(sk_code, sk_range)

        # Table Generation
        t = doc.add_table(2, len(levels))  # Create Table
        t.autofit = True
        t.style = 'Table Grid'
        t.alignment = docx.enum.table.WD_TABLE_ALIGNMENT.CENTER

        # Finding total length of descriptions for width calculations later
        total_description_length = 0
        for level in levels:
            total_description_length += len(level["description"])

        # Populating cells
        cell_count = 0
        for level in levels:
            top_cell = t.cell(0, cell_count).paragraphs[0].add_run('Level ' + str(level['level']))
            top_cell.bold = True
            top_cell.font.name = 'Calibri'
            bottom_cell = t.cell(1, cell_count).paragraphs[0].add_run(level['description'])
            bottom_cell.font.name = 'Calibri'
            bottom_cell.font.size = Pt(10)
            cell_width = 0.5 / len(levels) + 11.5 * len(level['description']) / total_description_length
            t.cell(0, cell_count).width = Inches(cell_width)
            t.cell(1, cell_count).width = Inches(cell_width)
            cell_count += 1

    def add_skill_info(sk_code):
        sk = get_skill(sk_code)
        p = doc.add_paragraph('')
        name = p.add_run(sk['name'] + ' ')
        name.bold = True
        name.font.size = Pt(14)
        name.font.name = 'Calibri'
        code = p.add_run(sk['code'])
        code.bold = True
        code.font.size = Pt(11)
        code.font.color.rgb = RGBColor(0x89, 0x89, 0x89)
        code.font.name = 'Calibri'
        description = p.add_run(' – ' + sk['description'])
        description.font.size = Pt(10)
        description.font.name = 'Calibri'

    def add_page_break():
        paragraph = doc.add_paragraph('')
        run = paragraph.add_run('')
        run.add_break(docx.enum.text.WD_BREAK.PAGE)

    # Generating the document
    if type=='employer':
        doc = docx.Document(settings.BASE_DIR + '/Generator/employer_template.docx')
    else:
        doc = docx.Document(settings.BASE_DIR + '/Generator/student_template.docx')
    # Adding skill information
    add_skill_info(sk1)
    # Adding the first table
    add_skill_table(sk1, [sk1_start, sk1_stop])
    # Addidng a page break
    add_page_break()
    # Adding skill information
    add_skill_info(sk2)
    # Adding the second table
    add_skill_table(sk2, [sk2_start, sk2_stop])

    # Saving to output
    filename = '%s-%s.docx' % (sk1,sk2)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    doc.save(response)

    return response