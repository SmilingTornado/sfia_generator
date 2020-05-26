# Create your views here.
import docx
import gensim
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from docx.shared import RGBColor, Inches, Pt
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Skill, Level


@csrf_exempt
def index(request):
    if request.method == "GET":
        context = {'searched': False}
        return render(request, 'form.html', context)
    elif request.method == "POST":
        if 'type' in request.POST and 'sk1' in request.POST and 'sk2' in request.POST \
                and 'sk1_min' in request.POST and 'sk2_min' in request.POST \
                and 'sk1_max' in request.POST and 'sk2_max' in request.POST:
            if is_valid(request):
                return generate(request)
            else:
                return render(request, 'invalid.html', {})

        elif 'input' in request.POST:
            return search_similarities(request)

        elif 'code_1' and 'code_2' in request.POST:
            context = {'searched': False, 'sk1_code': request.POST['code_1'], 'sk2_code': request.POST['code_2']}
            return render(request, 'form.html', context)

        else:
            return render(request, 'invalid.html', {})
    else:
        context = {'searched': False}
        return render(request, 'form.html', context)


def search_page(request):
    return render(request, 'search.html', {})


def list_skills(request):
    set_1 = []
    set_2 = []
    set_3 = []
    skill_objects = Skill.objects.all().order_by('code')
    length = len(skill_objects)
    for num, skill in enumerate(skill_objects, start=0):
        if num < length / 3:
            set_1.append(skill)
        elif num < length * (2 / 3):
            set_2.append(skill)
        else:
            set_3.append(skill)
    return render(request, 'list_skills.html', {"set_1": set_1, "set_2": set_2, "set_3": set_3})


def select_second(request, code_1):
    set_1 = []
    set_2 = []
    set_3 = []
    skill_objects = Skill.objects.all().order_by('code')
    length = len(skill_objects)
    for num, skill in enumerate(skill_objects, start=0):
        if num < length / 3:
            set_1.append(skill)
        elif num < length * (2 / 3):
            set_2.append(skill)
        else:
            set_3.append(skill)
    return render(request, 'list_skills.html', {"code_1": code_1, "set_1": set_1, "set_2": set_2, "set_3": set_3})


def show_skill(request, code):
    try:
        skill_object = Skill.objects.get(code=code.lower())
        levels = Level.objects.filter(skill=skill_object)
        skill = {
            'skill': skill_object,
            'levels': levels
        }
        return render(request, 'show_skill.html', skill)
    except:
        return render(request, 'invalid.html', {})


def view_second(request, code_1, code_2):
    try:
        skill_object = Skill.objects.get(code=code_2.lower())
        levels = Level.objects.filter(skill=skill_object)
        skill = {
            'skill': skill_object,
            'levels': levels,
            'code_1': code_1,
            'code_2': code_2
        }
        return render(request, 'show_skill.html', skill)
    except:
        return render(request, 'invalid.html', {})


def search_similarities(request):
    similarities = {}
    input = request.POST['input']
    gen_docs = [[w.lower() for w in word_tokenize(text)]
                for text in sent_tokenize(input)]
    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity(settings.BASE_DIR + '/Generator/gensim', tf_idf[corpus],
                                          num_features=len(dictionary))
    for level in Level.objects.all():
        skill_sim_total = 0

        for sentence in sent_tokenize(level.description):
            query_doc = [w.lower() for w in word_tokenize(sentence)]
            query_doc_bow = dictionary.doc2bow(query_doc)
            query_doc_tf_idf = tf_idf[query_doc_bow]
            sum_of_sims = (np.sum(sims[query_doc_tf_idf], dtype=np.float32))
            similarity = float(sum_of_sims / len(sent_tokenize(input)))
            skill_sim_total += similarity

        skill_sim = skill_sim_total / len(sent_tokenize(level.description))
        if level.skill.code not in similarities:
            similarities[level.skill.code] = skill_sim
        elif similarities[level.skill.code] < skill_sim:
            similarities[level.skill.code] = skill_sim
    for skill in Skill.objects.all():
        skill_sim_total = 0

        for sentence in sent_tokenize(skill.description):
            query_doc = [w.lower() for w in word_tokenize(sentence)]
            query_doc_bow = dictionary.doc2bow(query_doc)
            query_doc_tf_idf = tf_idf[query_doc_bow]
            sum_of_sims = (np.sum(sims[query_doc_tf_idf], dtype=np.float32))
            similarity = float(sum_of_sims / len(sent_tokenize(input)))
            skill_sim_total += similarity

        skill_sim = skill_sim_total / len(sent_tokenize(skill.description))
        if skill.code not in similarities:
            similarities[skill.code] = skill_sim
        elif similarities[skill.code] < skill_sim:
            similarities[skill.code] = skill_sim
    first_match = max(similarities, key=similarities.get)
    if (similarities[first_match] == 0):
        return render(request, 'form.html', {'searched': True})
    similarities.pop(first_match, None)
    second_match = max(similarities, key=similarities.get)
    if (similarities[second_match] == 0):
        return render(request, 'form.html', {'sk1_code': first_match.upper, 'searched': True})
    context = {'sk1_code': first_match.upper, 'sk2_code': second_match.upper, 'searched': True}
    return render(request, 'form.html', context)


def is_valid(request):
    sk1 = request.POST['sk1']
    sk1_start = int(request.POST['sk1_min'])
    sk1_stop = int(request.POST['sk1_max'])
    sk2 = request.POST['sk2']
    sk2_start = int(request.POST['sk2_min'])
    sk2_stop = int(request.POST['sk2_max'])
    type = request.POST['type']
    if 'type' in request.POST and 'sk1' in request.POST and 'sk2' in request.POST \
            and 'sk1_min' in request.POST and 'sk2_min' in request.POST \
            and 'sk1_max' in request.POST and 'sk2_max' in request.POST:
        if sk1_start >= 1 and sk2_start >= 1 and sk1_stop <= 7 and sk2_stop <= 7 and (
                type == 'student' or type == 'employer'):
            try:
                skill_object = Skill.objects.get(code=sk1.lower())
            except:
                return False
            if sk2 != '':
                try:
                    skill_object = Skill.objects.get(code=sk2.lower())
                except:
                    return False
            return True
        else:
            return False
    else:
        return False


def generate(request):
    sk1 = request.POST['sk1']
    sk1_start = int(request.POST['sk1_min'])
    sk1_stop = int(request.POST['sk1_max'])
    sk2 = request.POST['sk2']
    sk2_start = int(request.POST['sk2_min'])
    sk2_stop = int(request.POST['sk2_max'])
    type = request.POST['type']
    dedicate = False
    if 'dedicate' in request.POST:
        dedicate = True

    # Generating the document
    if type == 'employer':
        doc = docx.Document(settings.BASE_DIR + '/Generator/employer_template.docx')
    else:
        doc = docx.Document(settings.BASE_DIR + '/Generator/student_template.docx')
    if dedicate:
        # Addidng a page break
        add_page_break(doc)
    if sk2 != '':
        sk1_concat = ''.join(get_levels_list(sk1, [sk1_start, sk1_stop]))
        sk2_concat = ''.join(get_levels_list(sk2, [sk2_start, sk2_stop]))
        # Check if skill 1 is longer than skill 2
        if len(sk1_concat) <= len(sk2_concat):
            # Adding skill information
            add_skill_info(sk1, doc)
            # Adding the first table
            add_skill_table(sk1, [sk1_start, sk1_stop], doc)
            # Addidng a page break
            add_page_break(doc)
            # Adding skill information
            add_skill_info(sk2, doc)
            # Adding the second table
            add_skill_table(sk2, [sk2_start, sk2_stop], doc)
            filename = '%s-%s.docx' % (sk1.upper(), sk2.upper())
        else:
            # Adding skill information
            add_skill_info(sk2, doc)
            # Adding the first table
            add_skill_table(sk2, [sk2_start, sk2_stop], doc)
            # Addidng a page break
            add_page_break(doc)
            # Adding skill information
            add_skill_info(sk1, doc)
            # Adding the second table
            add_skill_table(sk1, [sk1_start, sk1_stop], doc)
            filename = '%s-%s.docx' % (sk2.upper(), sk1.upper())
    else:
        # Adding skill information
        add_skill_info(sk1, doc)
        # Adding the first table
        add_skill_table(sk1, [sk1_start, sk1_stop], doc)
        filename = '%s.docx' % (sk1.upper())

    # Saving to output
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    doc.save(response)
    return response


def get_skill(sk_code):
    skill_object = Skill.objects.get(code=sk_code.lower())

    skill = {
        'name': skill_object.name,
        'code': skill_object.code,
        'description': skill_object.description,
        'levels': []
    }
    for level in Level.objects.filter(skill=skill_object):
        skill['levels'].append({
            'level': level.level,
            'description': level.description,
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


def add_skill_table(sk_code, sk_range, doc):
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


def add_skill_info(sk_code, doc):
    sk = get_skill(sk_code)
    p = doc.add_paragraph('')
    name = p.add_run(sk['name'] + ' ')
    name.bold = True
    name.font.size = Pt(14)
    name.font.name = 'Calibri'
    code = p.add_run(sk['code'].upper())
    code.bold = True
    code.font.size = Pt(11)
    code.font.color.rgb = RGBColor(0x89, 0x89, 0x89)
    code.font.name = 'Calibri'
    description = p.add_run(' – ' + sk['description'])
    description.font.size = Pt(10)
    description.font.name = 'Calibri'


def add_page_break(doc):
    paragraph = doc.add_paragraph('')
    run = paragraph.add_run('')
    run.add_break(docx.enum.text.WD_BREAK.PAGE)


def get_levels_list(sk_code, sk_range):
    sk = get_skill(sk_code)
    levels = []

    for i in range(sk_range[0], sk_range[1] + 1):
        for level in sk['levels']:
            if level['level'] == i:
                levels.append(level['description'])
                break
    return levels
