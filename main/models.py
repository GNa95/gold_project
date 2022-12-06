# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from user.models import User


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CommunityMainboard(models.Model):
    area = models.CharField(max_length=8)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'community_mainboard'


class CommunityReply(models.Model):
    reply = models.TextField()
    created_dt = models.DateTimeField()
    post = models.ForeignKey(CommunityMainboard, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'community_reply'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TbEnt(models.Model):
    ent_num = models.IntegerField(db_column='ENT_NUM', primary_key=True)  # Field name made lowercase.
    ent_area_cd = models.ForeignKey('TbEntArea', models.DO_NOTHING, db_column='ENT_AREA_CD')  # Field name made lowercase.
    ent_type_cd = models.ForeignKey('TbEntType', models.DO_NOTHING, db_column='ENT_TYPE_CD')  # Field name made lowercase.
    ent_nm = models.CharField(db_column='ENT_NM', max_length=50)  # Field name made lowercase.
    ent_phone = models.CharField(db_column='ENT_PHONE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ent_post_no = models.CharField(db_column='ENT_POST_NO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ent_addr = models.CharField(db_column='ENT_ADDR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    map_x = models.FloatField(db_column='MAP_X')  # Field name made lowercase.
    map_y = models.FloatField(db_column='MAP_Y')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_ent'


class TbEntArea(models.Model):
    ent_area_cd = models.IntegerField(db_column='ENT_AREA_CD', primary_key=True)  # Field name made lowercase.
    ent_area_nm = models.CharField(db_column='ENT_AREA_NM', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_ent_area'


class TbEntType(models.Model):
    ent_type_cd = models.CharField(db_column='ENT_TYPE_CD', primary_key=True, max_length=2)  # Field name made lowercase.
    ent_type_nm = models.CharField(db_column='ENT_TYPE_NM', max_length=12)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_ent_type'


class TbGdCd(models.Model):
    gd_type_cd = models.CharField(db_column='GD_TYPE_CD', primary_key=True, max_length=10)  # Field name made lowercase.
    gd_type_1 = models.CharField(db_column='GD_TYPE_1', max_length=30)  # Field name made lowercase.
    gd_type_2 = models.CharField(db_column='GD_TYPE_2', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_gd_cd'


class TbGds(models.Model):
    gd_num = models.IntegerField(db_column='GD_NUM', primary_key=True)  # Field name made lowercase.
    gd_type_cd = models.ForeignKey(TbGdCd, models.DO_NOTHING, db_column='GD_TYPE_CD')  # Field name made lowercase.
    gd_nm = models.CharField(db_column='GD_NM', max_length=100)  # Field name made lowercase.
    gd_descd = models.CharField(db_column='GD_DESCD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    gd_unit = models.IntegerField(db_column='GD_UNIT', blank=True, null=True)  # Field name made lowercase.
    gd_unit_cd = models.ForeignKey('TbUnit', models.DO_NOTHING, db_column='GD_UNIT_CD')  # Field name made lowercase.
    gd_ent_nm = models.CharField(db_column='GD_ENT_NM', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_gds'


class TbIrdent(models.Model):
    recipe_num = models.ForeignKey('TbRecipe', models.DO_NOTHING, db_column='RECIPE_NUM', blank=True, null=True)  # Field name made lowercase.
    irdnt_nm = models.CharField(db_column='IRDNT_NM', max_length=50)  # Field name made lowercase.
    irdnt_type = models.CharField(db_column='IRDNT_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    gd_type_cd = models.ForeignKey(TbGdCd, models.DO_NOTHING, db_column='GD_TYPE_CD')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_irdent'


class TbRecipe(models.Model):
    recipe_num = models.IntegerField(db_column='RECIPE_NUM', primary_key=True)  # Field name made lowercase.
    recipe_nm = models.CharField(db_column='RECIPE_NM', max_length=40)  # Field name made lowercase.
    nation_cd = models.IntegerField(db_column='NATION_CD', blank=True, null=True)  # Field name made lowercase.
    nation_nm = models.CharField(db_column='NATION_NM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    type_cd = models.IntegerField(db_column='TYPE_CD', blank=True, null=True)  # Field name made lowercase.
    type_nm = models.CharField(db_column='TYPE_NM', max_length=25, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_recipe'


class TbUnit(models.Model):
    gd_unit_cd = models.CharField(db_column='GD_UNIT_CD', primary_key=True, max_length=4)  # Field name made lowercase.
    gd_unit_nm = models.CharField(db_column='GD_UNIT_NM', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_unit'


class TbUser(models.Model):
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(unique=True, max_length=100)
    user_id = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=40)
    user_addr = models.CharField(max_length=40)
    user_level = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'tb_user'


class ThSearch1(models.Model):
    user_id = models.CharField(max_length=30)
    recipe_nm = models.CharField(db_column='RECIPE_NM', max_length=50)  # Field name made lowercase.
    ht_date = models.DateTimeField(db_column='HT_DATE', auto_now_add=True, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'th_search1'


class ThSearch2(models.Model):
    search = models.ForeignKey('ThSearch1', on_delete=models.CASCADE)
    irdnt_nm = models.CharField(db_column='IRDNT_NM', max_length=50)  # Field name made lowercase.
    gd_nm = models.CharField(db_column='GD_NM', max_length=100)  # Field name made lowercase.

    class Meta:
        db_table = 'th_search2'