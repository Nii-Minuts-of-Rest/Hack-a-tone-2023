from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from .models import Question, Answer, Report, TagsGroup, Tag, Sentence
from .forms import UploadFileForm
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
import nltk
import pymorphy2
import re # добавлено удаление знаков препинания
from nltk.corpus import stopwords
from datetime import datetime as dtime
#from .process import html_to_pdf 


def start_app(request):
    return HttpResponseRedirect("/question/show")

def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES["file"])
            f = request.FILES["file"]
            result = bytearray()
            for chunk in f.chunks():
                result.extend(chunk)
            dfs = pd.read_excel(bytes(result))
            q = Question()
            q.question_text = dfs.columns[0]
            q.save()
            for i in range(len(dfs)):
                a = Answer()
                a.anwser_text = dfs.loc[i][0]
                a.answer_edited = dfs.loc[i][0]
                a.question_id = q
                a.save()
            
            return HttpResponseRedirect("/question/show")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})

def answer_function(request):
    if request.method == "POST":
        # Обработка ответа
        id = int(request.POST.get("q_id", ""))
        response_a = request.POST.get("answer", "")
        q = Question.objects.get(id=id)
        a = Answer()
        a.anwser_text = response_a
        a.answer_edited = response_a
        a.question_id = q
        a.save()
        return HttpResponse("Спасибо за Ваш ответ!")
        #return HttpResponseRedirect(f"/question/show?id={id}")
    elif request.method =='GET':
        questionId = int(request.GET.get("id", -1))
        if questionId < 0:
            return HttpResponseRedirect("/question/show")
        else:
            question_l = Question.objects.get(id=questionId)
            return render(request, "answer_here.html", {"question": question_l})
    else:
        return HttpResponse("Успокойся, хакер")

# Upload Menu
def add_question(request):
    if request.method == "POST":
        q = Question()
        q.question_text = request.POST.get("question_l", "")
        q.save()
        return HttpResponseRedirect("/question/show")
    elif request.method =='GET':
        return render(request, "add_q.html")
    else:
        return HttpResponse("Успокойся, хакер")
    

# Delete Question
def delete_question(request):
    questionId = int(request.GET.get("id", -1))
    if questionId < 0:
        return HttpResponseRedirect("/question/show")
    else:
        try:
            question_l = Question.objects.get(id=questionId)
            question_l.delete()
            return HttpResponseRedirect("/question/show")
        except Question.DoesNotExist:
            return HttpResponseRedirect("/question/show")

 # Questions List 
def questions(request):
    questionId = int(request.GET.get("id", -1))
    questions = Question.objects.all()
    
    
    if questionId < 0:
        return render(request, "question_list.html", {"questions": questions})
    else:
        questions = questions.filter(id=questionId)
        q = questions[0]
        answers = Answer.objects.filter(question_id=questionId)
        reports = Report.objects.filter(question_id=questionId)
        count = len(answers)
        return render(request, "question.html", {"question": q, "answers": answers, "count":count, "reports":reports})
 
# Question Answer List + Reports + Generate Report
def question(request):
    return HttpResponse("Конкретный вопрос, его ответы, отчёты + кнопка сгенерировать отчёт")

# Question Report
def report(request):
    return HttpResponse("Отчёт, распечатать, сделать презентацию")

 # Analisis Result
def contact(request):
    return HttpResponse("Контакты")

def edit_answer(request):
    if request.method =='POST':
        id = int(request.POST.get("id_ans", -1))
        new_ans = request.POST.get("new_answer", "")
        answer = Answer.objects.get(id=id)
        answer.answer_edited = new_ans
        answer.save()
        i = 0
        return HttpResponseRedirect(f"/question/show?id={int(answer.question_id.id)}")
    elif request.method =='GET':
        answerId = int(request.GET.get("id", -1))
        if answerId < 0:
            return HttpResponse("Не выбран ответ для редактирования")
        else:
            answers = Answer.objects.filter(id=answerId)
            ans = answers[0]
            return render(request, "edit_answer.html", {"answer":ans})
    else:
        return HttpResponse("Успокойся, хакер")

def start_analisis(request):
    questionId = int(request.GET.get("id", -1))
    if questionId < 0:
        return HttpResponse("Не выбран Вопрос для анализа")
    else:
        q = Question.objects.get(id=questionId)
        answers = Answer.objects.filter(question_id=questionId)
        data_array = list()
        for ans in answers:
            data_array.append(ans.answer_edited)
        # Обработка
        nltk.download('stopwords')
        stop_words = set(stopwords.words('russian'))
        data = pd.DataFrame(data_array)
        data[0] = data[0].fillna('')
        text = data[0].astype(str).tolist()
        text = [re.sub(r'[^\w\s]', '', doc) for doc in text]
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(text)
        feature_names = vectorizer.get_feature_names_out()
        morph = pymorphy2.MorphAnalyzer()
        text_tokenized = [[morph.parse(token)[0].normal_form for token in doc.split() if token not in stop_words] for doc in text]
        # Создание словаря для LDA
        dictionary = Dictionary(text_tokenized)
        # Преобразование текстов в мешки слов
        corpus = [dictionary.doc2bow(text) for text in text_tokenized]
        # Обучение модели LDA
        lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, passes=10, alpha='auto', eta='auto')
        result = lda.show_topics(num_topics=5, num_words=10, formatted=False)


        #print(len(result))
        #print(result[0])

        print(len(answers))

        R = Report()
        R.creation_date = dtime.now()
        R.data_count = len(answers)
        R.question_id = q
        R.save()

        used_words = {}

        for i, topic in result:
            TGroup = TagsGroup()
            TGroup.report_id = R
            TGroup.save()

            
            topic_words = []
            for word, _ in topic:
                # Проверка, что слово еще не было использовано
                if word not in used_words:
                    topic_words.append(word)
                    used_words[word] = True
                # Если слово уже было использовано, пропускаем его
                else:
                    continue
                # Если количество слов в топике достигло 10, выходим из цикла
                if len(topic_words) == 10:
                    break
            # Составление предложений
            for word in topic_words:
                tag_one = Tag()
                tag_one.tag_text = word
                tag_one.tagsGroup_id = TGroup
                tag_one.popularity = 0
                tag_one.save()


            sentences = set()
            for sentence in text:
                words_in_sentence = set(sentence.split())
                if len(words_in_sentence.intersection(topic_words)) > 0 and sentence not in sentences:
                    sentences.add(sentence)
                if len(sentences) == 2:
                    break
            for sentence in sentences:
                snts = Sentence()
                snts.sentence_text = sentence
                snts.tagsGroup_id = TGroup
                snts.save()
        return HttpResponseRedirect(f"/question/show?id={questionId}")
    
def showReport(request):
    if request.method =='GET':
        id = int(request.GET.get("id", -1))
        if id < 0:
            return HttpResponse("Не выбран отчёт")
        else:
            #return HttpResponse("Выбран отчёт")
            R = Report.objects.get(id=id)
            Q = Question.objects.get(id=R.question_id.id)
            TGr = TagsGroup.objects.filter(report_id=R.id)
            listq = list()
            for t in TGr:
                listq.append(t.id)
            
            print(listq)
            TGs = Tag.objects.filter(tagsGroup_id__in=listq)
            print(TGs)

            Snts = Sentence.objects.filter(tagsGroup_id__in=listq)
            print(Snts)
            #AllTags = Tag.objects.filter(id=TGr[0].id).filter(id=TGr[1].id).filter(id=TGr[2].id).filter(id=TGr[3].id).filter(id=TGr[4].id)
            #for Rrr in TGr:
                
            #    AllTags.append(TGs)
            #print(len(AllTags))

            return render(request, "report.html", { "report":R, "question": Q, "TagGroups":TGr, "Tags":TGs, "Sentences": Snts}) #, "answers": answers, "count":count,
            #return HttpResponse("Выбран отчёт")
    else:
        return HttpResponse("Успокойся, хакер")

#class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
         
        # getting the template
#        pdf = html_to_pdf('result.html')
         
         # rendering the template
#        return HttpResponse(pdf, content_type='application/pdf')