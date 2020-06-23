# -*- coding: UTF-8 -*- 


from dictionary.models import Kanji

badge_list = {
    'money man' : {
        'task' : 'Earn 100 yen',
        'label' : '💰',
    },
    'super saver' : {
        'task' : 'Earn 1000 yen',
        'label' : '💴',
    },
    'high roller' :{
        'task' : 'Earn 5,000 yen',
        'label' : '💸',
    },
    'boss man' :{
        'task' : 'Earn 10,000 yen',
        'label' : '🤑',
    },
    'kanji baby' :{
        'task' : 'master 10 kanji',
        'label' : '👶',
    },
    'kanji boy' :{
        'task' : 'master 100 kanji',
        'label' : '👦',
    },
    'kanji man' :{
        'task' : 'master 500 kanji',
        'label' : '👲',
    },
    'kanji king' :{
        'task' : 'master 1000 kanji',
        'label' : '🤴',
    },
    'word smith' :{
        'task' : 'master 50 words',
        'label' : '🤠',
    },
    'word wonder' :{
        'task' : 'master 250 words',
        'label' : '🤖',
    },
    'word wizard' :{
        'task' : 'master 1000 words',
        'label' : '🧙',
    },
    'word God' :{
        'task' : 'master 2000 words',
        'label' : '🤯',
    },
    'One-derful Student' : {
        'task' : 'Master all first grade kanji',
        'label' : '👨‍💻',
    },
    'Two Cool' : {
        'task' : 'Master all second grade kanji',
        'label' : '😎',
    },
    'Bruce Three' : {
        'task' : 'Master all third grade kanji',
        'label' : '🥋',
    },
    'Krazy Four Kanji' : {
        'task' : 'Master all fourth grade kanji',
        'label' : '🤪',
    },
    'High Five' : {
        'task' : 'Master all fifth grade kanji',
        'label' : '🖐️',
    },
    'I\'m Too Six-y' : {
        'task' : 'Master all sixth grade kanji',
        'label' : '🧜‍♂️',
    },
    'Stairway to Seven' : {
        'task' : 'Master all seventh grade kanji',
        'label' : '🌌',
    },
    'Eight Baller' : {
        'task' : 'Master all eigth grade kanji',
        'label' : '🎱',
    },
    'word walker' :{
        'task' : 'master 5 kanji containing the leg (儿)  radical',
        'label' : '🚶‍',
    },
    'Mr. White' :{
        'task' : 'master 5 kanji containing the white (白)  radical',
        'label' : '💀',
    },
    'earth worm' :{
        'task' : 'master 10 kanji containing the ground (土)  radical',
        'label' : '🐛',
    },
    'solar flare' :{
        'task' : 'master 15 kanji containing the sun (日)  radical',
        'label' : '🌞',
    },
    'thirsty boy' :{
        'task' : 'master 5 kanji containing the water (水)  radical',
        'label' : '😓',
    },
    'hott stuff' :{
        'task' : 'master 5 kanji containing the fire (火)  radical',
        'label' : '🔥',
    },
    'ghost slayer' :{
        'task' : 'master 10 kanji containing the corpse (尸)  radical',
        'label' : '👻',
    },
    'ninja' :{
        'task' : 'master 10 kanji containing the sword (刀)  radical ',
        'label' : '🐱‍👤',
    },

}


def check_if_badge_earned(badge_name, oUser):
    if badge_name == 'One-derful Student':
        return True if oUser.check_grade_complete(1) else False
    if badge_name == 'Two Cool':
        return True if oUser.check_grade_complete(2) else False
    if badge_name == 'Bruce Three':
        return True if oUser.check_grade_complete(3) else False
    if badge_name == 'Krazy Four Kanji':
        return True if oUser.check_grade_complete(4) else False
    if badge_name == 'High Five':
        return True if oUser.check_grade_complete(5) else False
    if badge_name == 'I\'m Too Six-y':
        return True if oUser.check_grade_complete(6) else False
    if badge_name == 'Stairway to Seven':
        return True if oUser.check_grade_complete(6) else False # there aren't any grade 7 kanji
    if badge_name == 'Eight Baller':
        return True if oUser.check_grade_complete(8) else False
    if badge_name == 'money man':
        return True if oUser.score >= 100 else False
    if badge_name == 'super saver':
        return True if oUser.score >= 1000 else False
    if badge_name == 'high roller':
        return True if oUser.score >= 5000 else False
    if badge_name == 'boss man':
        return True if oUser.score >= 10000 else False
    if badge_name == 'kanji baby':
        return True if oUser.count_completed_kanji() >= 10 else False
    if badge_name == 'kanji boy':
        return True if oUser.count_completed_kanji() >= 100 else False
    if badge_name == 'kanji man':
        return True if oUser.count_completed_kanji() >= 500 else False
    if badge_name == 'kanji king':
        return True if oUser.count_completed_kanji() >= 1000 else False
    if badge_name == 'word smith':
        return True if oUser.count_completed_words() >= 50 else False
    if badge_name == 'word wonder':
        return True if oUser.count_completed_words() >= 250 else False
    if badge_name == 'word wizard':
        return True if oUser.count_completed_words() >= 1000 else False
    if badge_name == 'word god':
        return True if oUser.count_completed_words() >= 2000 else False
    if badge_name == 'word_walker':
        return True if Kanji.objects.filter(radicals__character='儿').filter(
            concept__conceptuser__user=oUser    
        ).count() >= 5 else False
    if badge_name == 'Mr. White':
        return True if Kanji.objects.filter(radicals__character='白').filter(
            concept__conceptuser__user=oUser    
        ).count() >= 5 else False
    if badge_name == 'earth worm':
        return True if Kanji.objects.filter(radicals__character='土').filter(
            concept__conceptuser__user=oUser    
        ).count() >= 10 else False
    if badge_name == 'solar flare':
        return True if Kanji.objects.filter(radicals__character='日').filter(
            concept__conceptuser__user=oUser    
        ).count() >= 15 else False
    if badge_name == 'thirsty boy':
        return True if Kanji.objects.filter(radicals__character='水').filter(
            concept__conceptuser__user=oUser    
        ).count() >= 5 else False
    if badge_name == 'hott stuff':
        return True if Kanji.objects.filter(radicals__character='火').filter(
            concept__conceptuser__user=oUser    
        ).count() >= 5 else False
    if badge_name == 'ghost slayer':
        return True if Kanji.objects.filter(radicals__character='尸').filter(
            concept__conceptuser__user=oUser    
        ).count() >= 10 else False
    if badge_name == 'ninja':
        return True if Kanji.objects.filter(radicals__character='刀').filter(
            concept__conceptuser__user=oUser    
        ).count() >= 10 else False
            










