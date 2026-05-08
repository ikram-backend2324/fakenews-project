from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from detector.models import Analysis


SEED_USERS = [
    {
        'username': 'admin',
        'email': 'admin@fakenews-ai.com',
        'password': 'Admin1234!',
        'first_name': 'Admin',
        'is_staff': True,
        'is_superuser': True,
    },
    {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'Alice1234!',
        'first_name': 'Alice',
        'is_staff': False,
        'is_superuser': False,
    },
    {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'Bob12345!',
        'first_name': 'Bob',
        'is_staff': False,
        'is_superuser': False,
    },
]

SEED_ANALYSES = [
    {
        'username': 'alice',
        'news_text': 'Scientists at NASA have confirmed the discovery of liquid water on Mars, with evidence of an underground lake detected by the MARSIS radar on the Mars Express spacecraft. This is considered a major breakthrough in the search for extraterrestrial life.',
        'verdict': 'real',
        'confidence': 92,
        'reasoning': 'This news is consistent with verified scientific reports from 2018 published in Science journal. The MARSIS radar finding was a peer-reviewed discovery announced by the European Space Agency. The language is measured and scientific.',
        'language_used': 'en',
    },
    {
        'username': 'alice',
        'news_text': 'BREAKING: 5G towers are secretly emitting mind-control frequencies that cause people to become obedient to the global elite. Scientists who tried to speak out have been silenced. Share this before it gets deleted!',
        'verdict': 'fake',
        'confidence': 98,
        'reasoning': 'This article exhibits multiple hallmarks of disinformation: sensationalist language, conspiracy framing, vague attribution ("scientists"), and an urgent call to share. The claim about 5G mind control has no scientific basis and has been debunked repeatedly.',
        'language_used': 'en',
    },
    {
        'username': 'bob',
        'news_text': 'Учёные из Оксфордского университета утверждают, что употребление кофе может снизить риск развития болезни Альцгеймера на 65%. Исследование охватило более 50 000 участников в течение 10 лет.',
        'verdict': 'uncertain',
        'confidence': 55,
        'reasoning': 'Хотя некоторые исследования действительно связывают потребление кофе с потенциальной защитой от нейродегенеративных заболеваний, заявленный процент в 65% кажется чрезмерно высоким. Невозможно проверить конкретные детали исследования без оригинальной ссылки.',
        'language_used': 'ru',
    },
    {
        'username': 'bob',
        'news_text': 'SHOSHILINCH: Prezident ertaga barcha fuqarolarning bank hisoblarini muzlatishni buyurdi. Pulingizni zudlik bilan naqd qilib oling! Bu xabarni o\'chirishdan oldin ulashing!',
        'verdict': 'fake',
        'confidence': 99,
        'reasoning': 'Bu yangilik klassik dezinformatsiya belgilarini ko\'rsatadi: o\'ta shoshilinch til, manblar yo\'qligi va darhol harakat qilishga da\'vat. Bunday muhim moliyaviy qarorlar rasmiy kanallar orqali e\'lon qilinadi.',
        'language_used': 'uz',
    },
    {
        'username': 'alice',
        'news_text': 'The World Health Organization has issued new guidelines recommending that adults get at least 150 minutes of moderate physical activity per week. The updated recommendations emphasize the importance of reducing sedentary behavior.',
        'verdict': 'real',
        'confidence': 95,
        'reasoning': 'This accurately reflects the WHO physical activity guidelines which are publicly available. The recommendation of 150 minutes of moderate activity weekly is well-documented. The language is professional and matches official health communication standards.',
        'language_used': 'en',
    },
    {
        'username': 'bob',
        'news_text': 'Local hospital reports a 300% increase in emergency visits after residents consumed tap water this week. City officials deny any contamination despite multiple complaints from citizens.',
        'verdict': 'uncertain',
        'confidence': 45,
        'reasoning': 'While water contamination events do occur, this article lacks specific details such as the hospital name, city, or official reports. The 300% figure is specific but unverified. This could be real but requires verification from official sources.',
        'language_used': 'en',
    },
    {
        'username': 'alice',
        'news_text': 'Новое исследование показало, что социальные сети усиливают тревожность у подростков. Исследователи из Стэнфордского университета проанализировали данные 10 000 участников в возрасте 13-18 лет.',
        'verdict': 'real',
        'confidence': 82,
        'reasoning': 'Связь между использованием социальных сетей и тревожностью у подростков хорошо задокументирована в научной литературе. Стэнфордский университет активно изучает эту тему. Статья написана в умеренном академическом тоне.',
        'language_used': 'ru',
    },
    {
        'username': 'bob',
        'news_text': 'O\'zbekistonda yangi valyuta joriy etildi: 1 so\'m endi 1 dollarga teng bo\'ladi. Markaziy bank bu o\'zgarishlar 2025-yildan kuchga kirishini tasdiqladi.',
        'verdict': 'fake',
        'confidence': 97,
        'reasoning': 'Bu da\'vo mutlaqo asossiz: valyuta almashinuvi bunday tez o\'zgarmaydi va bunday muhim qaror rasmiy hukumat kanallarida keng yoritilgan bo\'lardi. Maqolada hech qanday rasmiy manba ko\'rsatilmagan.',
        'language_used': 'uz',
    },
    {
        'username': 'alice',
        'news_text': 'Apple announces record quarterly revenue of $119.6 billion, driven by strong iPhone 15 sales and services growth. The company also reported a 13% increase in services revenue year-over-year.',
        'verdict': 'real',
        'confidence': 90,
        'reasoning': 'Apple regularly reports quarterly earnings and the figures cited align with publicly available financial reports. Revenue milestones of this magnitude are covered extensively by financial media and verified through SEC filings.',
        'language_used': 'en',
    },
    {
        'username': 'bob',
        'news_text': 'СРОЧНО: Правительство планирует ввести налог на интернет в размере 50% с 1 января. Все сайты будут платными. Успейте сохранить нужные страницы!',
        'verdict': 'fake',
        'confidence': 99,
        'reasoning': 'Статья использует типичные признаки дезинформации: слово "срочно", отсутствие конкретных источников, нереалистичные заявления и призыв к немедленным действиям. Подобные изменения потребовали бы законодательных процедур и широкого освещения в прессе.',
        'language_used': 'ru',
    },
]


class Command(BaseCommand):
    help = 'Seed the database with demo users and analyses'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('🌱 Seeding database...'))

        # Create users
        created_users = {}
        for user_data in SEED_USERS:
            username = user_data['username']
            if User.objects.filter(username=username).exists():
                self.stdout.write(f'  ⚡ User "{username}" already exists, skipping.')
                created_users[username] = User.objects.get(username=username)
                continue

            user = User.objects.create_user(
                username=username,
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                is_staff=user_data['is_staff'],
                is_superuser=user_data['is_superuser'],
            )
            UserProfile.objects.get_or_create(user=user)
            created_users[username] = user
            self.stdout.write(self.style.SUCCESS(f'  ✅ Created user: {username}'))

        # Create analyses
        analysis_count = 0
        for data in SEED_ANALYSES:
            owner = created_users.get(data['username'])
            if not owner:
                continue
            # Avoid duplicate seeding
            if Analysis.objects.filter(user=owner, news_text=data['news_text']).exists():
                continue
            Analysis.objects.create(
                user=owner,
                news_text=data['news_text'],
                verdict=data['verdict'],
                confidence=data['confidence'],
                reasoning=data['reasoning'],
                language_used=data['language_used'],
                processing_time=round(1.2 + analysis_count * 0.3, 2),
            )
            analysis_count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {analysis_count} analyses'))
        self.stdout.write(self.style.SUCCESS('\n🎉 Seed complete!'))
        self.stdout.write('')
        self.stdout.write('  Admin credentials:')
        self.stdout.write('    Username: admin')
        self.stdout.write('    Password: Admin1234!')
        self.stdout.write('')
        self.stdout.write('  Demo users:')
        self.stdout.write('    alice / Alice1234!')
        self.stdout.write('    bob   / Bob12345!')
