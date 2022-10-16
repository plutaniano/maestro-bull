# Generated by Django 3.2.13 on 2022-06-30 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Captacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office', models.CharField(max_length=128, verbose_name='Escritório')),
                ('date', models.DateField(verbose_name='Data')),
                ('type', models.CharField(choices=[('cbx', 'CBX'), ('cex', 'CEX'), ('coe', 'COE'), ('cpj', 'CPJ'), ('fixed_income', 'Renda Fixa'), ('ota', 'OTA'), ('pco_funds', 'Fundos PCO'), ('private_pension', 'Previdência'), ('private_pension_internal', 'Previdência Interna'), ('st', 'ST'), ('stvm', 'STVM'), ('ted', 'TED'), ('treasure', 'TD')], max_length=32, verbose_name='Tipo de Captação')),
                ('aux', models.CharField(choices=[('deposit', 'Entrada'), ('withdrawal', 'Saída')], max_length=16, verbose_name='Aux')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Captação')),
            ],
            options={
                'verbose_name': 'Captação',
                'verbose_name_plural': 'Captações',
            },
        ),
        migrations.CreateModel(
            name='CSVRevenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classification', models.CharField(choices=[('revenue', 'Receitas'), ('adjustment', 'Ajustes')], max_length=32, verbose_name='Classificação')),
                ('category', models.CharField(choices=[('anticipation_reversal', 'Estorno Adiantamento'), ('co_brokerage', 'Co-corretagem'), ('Crédito Colateralizado', 'Crédito Colateralizado'), ('express_withdrawal', 'Resgate Express'), ('forex', 'Câmbio'), ('guarantee', 'Seguro Garantia'), ('life_insurance', 'Vida'), ('pre_approved_incentives', 'Incentivos Pré-Aprovados'), ('private_pension', 'Previdência'), ('private_pension_advance', 'Adiantamento Previdência')], max_length=64, verbose_name='Categoria')),
                ('level_1', models.CharField(blank=True, max_length=128, null=True, verbose_name='Nível 1')),
                ('level_2', models.CharField(blank=True, max_length=128, null=True, verbose_name='Nível 2')),
                ('level_3', models.CharField(blank=True, max_length=128, null=True, verbose_name='Nível 3')),
                ('level_4', models.CharField(blank=True, max_length=128, null=True, verbose_name='Nível 4')),
                ('date', models.DateField(verbose_name='Data')),
                ('gross_revenue', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True, verbose_name='Receita Bruta')),
                ('liquid_revenue', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True, verbose_name='Receita Líquida')),
                ('comission_pct', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Comissão do Escritório (%)')),
                ('comission', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Comissão do Escritório (R$)')),
            ],
            options={
                'verbose_name': 'Receita CSV',
                'verbose_name_plural': 'Receitas CSV',
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='Positivador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Data')),
                ('occupation', models.CharField(max_length=256, verbose_name='Profissão')),
                ('sex', models.CharField(blank=True, choices=[('m', 'Masculino'), ('f', 'Feminino')], max_length=1, null=True, verbose_name='Sexo')),
                ('segment', models.CharField(blank=True, choices=[('private', 'Private'), ('express', 'Express'), ('unique', 'Unique'), ('plus', 'Plus'), ('not_available', 'Não disponível')], max_length=64, null=True, verbose_name='Segmento')),
                ('sign_up_date', models.DateField(verbose_name='Data de Cadastro')),
                ('made_second_deposit', models.BooleanField(verbose_name='Fez segundo aporte?')),
                ('birth_date', models.DateField(verbose_name='Data de Nascimento')),
                ('is_active', models.BooleanField(verbose_name='Status')),
                ('actived', models.BooleanField(verbose_name='Ativou em M?')),
                ('evaded', models.BooleanField(verbose_name='Evadiu em M?')),
                ('traded_bovespa', models.BooleanField(verbose_name='Operou Bolsa?')),
                ('traded_fund', models.BooleanField(verbose_name='Operou Fundo?')),
                ('traded_fixed_income', models.BooleanField(verbose_name='Operou Renda Fixa?')),
                ('declared_financial_investments', models.DecimalField(decimal_places=2, max_digits=36, verbose_name='Aplicação Financeira Declarada')),
                ('revenue', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Receita no Mês')),
                ('revenue_bovespa', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Receita Bovespa')),
                ('revenue_future', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Receita Futuros')),
                ('revenue_fixed_income_banking', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Receita RF Bancários')),
                ('revenue_fixed_income_private', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Receita RF Privados')),
                ('revenue_fixed_income_public', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Receita RF Públicos')),
                ('deposits_gross', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Captação Bruta em M')),
                ('withdrawals', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Resgate em M')),
                ('deposits_liquid', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Captação Líquida em M')),
                ('deposits_ted', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Captação TED')),
                ('deposits_st', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Captação ST')),
                ('deposits_ota', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Captação OTA')),
                ('deposits_fixed_income', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Captação OTA')),
                ('deposits_treasure', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Captação OTA')),
                ('deposits_private_pension', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Captação OTA')),
                ('patrimony_last_month', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Net em M-1')),
                ('patrimony', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Net em M')),
                ('patrimony_fixed_income', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Net Renda Fixa')),
                ('patrimony_real_estate', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Net Fundos Imobiliários')),
                ('patrimony_equity', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Net Renda Váriavel')),
                ('patrimony_fund', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Net Fundos')),
                ('patrimony_balance', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Net Financeiro')),
                ('patrimony_private_pension', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Net Previdência')),
                ('patrimony_other', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Net Outros')),
                ('revenue_rental', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Receita Aluguel')),
                ('revenue_complement', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Receita Complemento/Pacote Corretagem')),
            ],
            options={
                'verbose_name': 'Positivador',
                'verbose_name_plural': 'Positivadores',
                'ordering': ['-date'],
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='RelatorioMensal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classification', models.CharField(choices=[('revenue', 'Receitas'), ('adjustment', 'Ajustes')], max_length=32, verbose_name='Classificação')),
                ('category', models.CharField(choices=[('funds_admin_fee', 'Fundos - Taxa de Administração'), ('funds_campaign', 'Campanha Fundos'), ('funds_performance_fee', 'Fundos - Taxa de Performance'), ('exclusive_funds', 'Fundos Exclusivos'), ('coe', 'COE'), ('coe_campaign', 'Campanha COE'), ('fixed_fee', 'Fee Fixo'), ('fixed_income', 'Renda Fixa'), ('fixed_income_campaign', 'Campanha Renda Fixa'), ('fixed_income_ipo_fee', 'IPO Fee Renda Fixa'), ('real_estate_campaign', 'Campanha Fundos Imobiliários'), ('real_estate_offering', 'FII - Oferta'), ('bmf', 'BM&F'), ('bmf_mini', 'BM&F Mini'), ('bmf_self_service', 'BMF Self Service'), ('bovespa', 'Bovespa'), ('bovespa_self_service', 'Bovespa Self Service'), ('btc', 'BTC'), ('clubs', 'Clubes'), ('clubs_debit', 'Clubes (débito)'), ('customer_referral', 'Indicação de Clientes'), ('customer_transfer_penalty', 'Desconto de Transferência de Clientes'), ('equity_offering', 'Oferta RV'), ('managed_portfolio', 'Carteira Administrada'), ('operational_error', 'Erro Operacional'), ('primary_funds_distribution', 'Distribuição Primária de Fundos'), ('rlp_adjustment', 'Enquadramento RLP'), ('structured_campaign', 'Campanhas Estruturadas'), ('pre_approved_incentives', 'Incentivos Pré-Aprovados'), ('receipt_difference', 'Diferença de Nota Fiscal'), ('other_adjustments', 'Outros Ajustes')], max_length=32, verbose_name='Categoria')),
                ('level_1', models.CharField(blank=True, max_length=128, null=True, verbose_name='Nível 1')),
                ('level_2', models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='Nível 2')),
                ('level_3', models.CharField(blank=True, max_length=128, null=True, verbose_name='Nível 3')),
                ('date', models.DateField(verbose_name='Data')),
                ('gross_revenue', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True, verbose_name='Receita Bruta')),
                ('liquid_revenue', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True, verbose_name='Receita Líquida')),
                ('comission_pct', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Comissão do Escritório (%)')),
                ('comission', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Comissão do Escritório (R$)')),
            ],
            options={
                'verbose_name': 'Relatório Mensal',
                'verbose_name_plural': 'Relatórios Mensais',
            },
        ),
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('coe', 'COE'), ('credit', 'Crédito'), ('equity', 'Renda Variável'), ('real_estate', 'Fundos de Investimento Imobiliário'), ('fixed_income', 'Renda Fixa'), ('forex', 'Câmbio'), ('fund', 'Fundos de Investimento'), ('insurance', 'Seguros'), ('private_pension', 'Previdência'), ('other', 'Outros')], max_length=32, verbose_name='Categoria')),
                ('date', models.DateField(verbose_name='Data')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Quantidade')),
            ],
            options={
                'verbose_name': 'Receita',
                'verbose_name_plural': 'Receitas',
                'get_latest_by': 'date',
            },
        ),
    ]
