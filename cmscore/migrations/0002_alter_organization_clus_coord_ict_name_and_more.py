# Generated by Django 4.1.6 on 2023-03-20 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmscore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='Clus_Coord_ICT_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='Clus_Coord_R_and_D_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='Clus_Coord_Sci_Com_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='Clus_Coord_Tech_Trans_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='EXBM_DA_RFO_IX_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='EXBM_JHCSC_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='EXBM_PHILFIDA_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='EXBM_ZSCMST_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='EXMB_DA_BAR_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='Management_sup1_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='Management_sup2_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='Management_sup3_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='Management_sup4_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='WESMAARRDEC_Dir_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='depu_di_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='dostpcaarrd_ExDi_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='wmsupres_rrdcchair_exdi_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
