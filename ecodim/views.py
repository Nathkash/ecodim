from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Classe, Enfant, Lecon, Seance, PresenceEnfant, PresenceMoniteur
from datetime import date


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Identifiant ou mot de passe incorrect.')
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    context = {}

    if user.is_president():
        context['total_enfants'] = Enfant.objects.filter(actif=True).count()
        context['total_moniteurs'] = User.objects.filter(role='moniteur').count()
        context['prochaines_lecons'] = Lecon.objects.filter(
            statut='a_venir', date__gte=date.today()
        ).order_by('date')[:5]
        context['dernieres_seances'] = Seance.objects.all()[:3]
        context['classes'] = Classe.objects.all()
    else:
        classes = user.classes_assignees.all()
        context['mes_classes'] = classes
        context['mes_lecons'] = Lecon.objects.filter(
            moniteur_assigne=user, date__gte=date.today()
        ).order_by('date')[:5]

    return render(request, 'dashboard.html', context)


@login_required
def moniteurs_list(request):
    if not request.user.is_president():
        return redirect('dashboard')
    moniteurs = User.objects.filter(role='moniteur')
    return render(request, 'moniteurs/list.html', {'moniteurs': moniteurs})


@login_required
def moniteur_ajouter(request):
    if not request.user.is_president():
        return redirect('dashboard')
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            telephone=request.POST.get('telephone', ''),
            role='moniteur'
        )
        messages.success(request, f'Moniteur {user.first_name} créé avec succès !')
        return redirect('moniteurs_list')
    return render(request, 'moniteurs/form.html')


@login_required
def moniteur_detail(request, pk):
    moniteur = get_object_or_404(User, pk=pk, role='moniteur')
    lecons = Lecon.objects.filter(moniteur_assigne=moniteur).order_by('-date')
    return render(request, 'moniteurs/detail.html', {'moniteur': moniteur, 'lecons': lecons})


@login_required
def enfants_list(request):
    if request.user.is_president():
        enfants = Enfant.objects.filter(actif=True)
    else:
        classes = request.user.classes_assignees.all()
        if classes.filter(nom='A').exists() and classes.filter(nom='B').exists():
            enfants = Enfant.objects.filter(actif=True)
        elif classes.filter(nom='A').exists():
            enfants = Enfant.objects.filter(actif=True, date_naissance__gte=date.today().replace(year=date.today().year - 7))
        else:
            enfants = Enfant.objects.filter(actif=True, date_naissance__lt=date.today().replace(year=date.today().year - 7))
    return render(request, 'enfants/list.html', {'enfants': enfants})


@login_required
def enfant_ajouter(request):
    if request.method == 'POST':
        Enfant.objects.create(
            nom=request.POST['nom'],
            prenom=request.POST['prenom'],
            date_naissance=request.POST['date_naissance'],
            nom_parent=request.POST.get('nom_parent', ''),
            telephone_parent=request.POST.get('telephone_parent', ''),
        )
        messages.success(request, 'Enfant ajouté avec succès !')
        return redirect('enfants_list')
    return render(request, 'enfants/form.html')


@login_required
def enfant_detail(request, pk):
    enfant = get_object_or_404(Enfant, pk=pk)
    presences = PresenceEnfant.objects.filter(enfant=enfant).order_by('-seance__date')
    return render(request, 'enfants/detail.html', {'enfant': enfant, 'presences': presences})


@login_required
def enfant_modifier(request, pk):
    enfant = get_object_or_404(Enfant, pk=pk)
    if request.method == 'POST':
        enfant.nom = request.POST['nom']
        enfant.prenom = request.POST['prenom']
        enfant.date_naissance = request.POST['date_naissance']
        enfant.nom_parent = request.POST.get('nom_parent', '')
        enfant.telephone_parent = request.POST.get('telephone_parent', '')
        enfant.save()
        messages.success(request, 'Informations mises à jour !')
        return redirect('enfant_detail', pk=pk)
    return render(request, 'enfants/form.html', {'enfant': enfant})


@login_required
def lecons_list(request):
    if request.user.is_president():
        lecons = Lecon.objects.all()
    else:
        lecons = Lecon.objects.filter(moniteur_assigne=request.user)
    return render(request, 'lecons/list.html', {'lecons': lecons})


@login_required
def lecon_ajouter(request):
    if not request.user.is_president():
        return redirect('dashboard')
    if request.method == 'POST':
        Lecon.objects.create(
            titre=request.POST['titre'],
            theme=request.POST.get('theme', ''),
            reference_biblique=request.POST.get('reference_biblique', ''),
            date=request.POST['date'],
            classe=Classe.objects.get(pk=request.POST['classe']),
            moniteur_assigne=User.objects.get(pk=request.POST['moniteur_assigne']),
            statut='a_venir',
            created_by=request.user
        )
        messages.success(request, 'Leçon créée et assignée avec succès !')
        return redirect('lecons_list')
    
    classes = Classe.objects.all()
    moniteurs = User.objects.filter(role='moniteur')
    return render(request, 'lecons/form.html', {'classes': classes, 'moniteurs': moniteurs})


@login_required
def lecon_detail(request, pk):
    lecon = get_object_or_404(Lecon, pk=pk)
    return render(request, 'lecons/detail.html', {'lecon': lecon})


@login_required
def lecon_modifier(request, pk):
    if not request.user.is_president():
        return redirect('dashboard')
    lecon = get_object_or_404(Lecon, pk=pk)
    if request.method == 'POST':
        lecon.titre = request.POST['titre']
        lecon.theme = request.POST.get('theme', '')
        lecon.reference_biblique = request.POST.get('reference_biblique', '')
        lecon.date = request.POST['date']
        lecon.classe = Classe.objects.get(pk=request.POST['classe'])
        lecon.moniteur_assigne = User.objects.get(pk=request.POST['moniteur_assigne'])
        lecon.statut = request.POST['statut']
        lecon.save()
        messages.success(request, 'Leçon mise à jour !')
        return redirect('lecons_list')
    classes = Classe.objects.all()
    moniteurs = User.objects.filter(role='moniteur')
    return render(request, 'lecons/form.html', {'lecon': lecon, 'classes': classes, 'moniteurs': moniteurs})


@login_required
def presences_list(request):
    seances = Seance.objects.all()
    return render(request, 'presences/list.html', {'seances': seances})


@login_required
def nouvelle_seance(request):
    if not request.user.is_president():
        return redirect('dashboard')
    if request.method == 'POST':
        seance, created = Seance.objects.get_or_create(date=request.POST['date'])
        if created:
            messages.success(request, 'Nouvelle séance créée !')
        return redirect('presence_seance', pk=seance.pk)
    return render(request, 'presences/nouvelle_seance.html')


@login_required
def presence_seance(request, pk):
    seance = get_object_or_404(Seance, pk=pk)
    enfants = Enfant.objects.filter(actif=True)
    moniteurs = User.objects.filter(role='moniteur')

    already_saved = PresenceEnfant.objects.filter(seance=seance).exists()

    if request.method == 'POST' and not already_saved:
        for enfant in enfants:
            present = f'enfant_{enfant.pk}' in request.POST
            PresenceEnfant.objects.update_or_create(
                seance=seance, enfant=enfant,
                defaults={'present': present}
            )
        for moniteur in moniteurs:
            present = f'moniteur_{moniteur.pk}' in request.POST
            PresenceMoniteur.objects.update_or_create(
                seance=seance, moniteur=moniteur,
                defaults={'present': present}
            )
        messages.success(request, 'Présences enregistrées avec succès !')
        return redirect('presence_seance', pk=pk)

    presences_enfants = {
        p.enfant_id: p.present
        for p in PresenceEnfant.objects.filter(seance=seance)
    }
    presences_moniteurs = {
        p.moniteur_id: p.present
        for p in PresenceMoniteur.objects.filter(seance=seance)
    }

    return render(request, 'presences/seance.html', {
        'seance': seance,
        'enfants': enfants,
        'moniteurs': moniteurs,
        'presences_enfants': presences_enfants,
        'presences_moniteurs': presences_moniteurs,
        'already_saved': already_saved,
    })