PGDMP     "    +                z            skydb    14.2    14.1 8    W           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            X           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            Y           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            Z           1262    21520    skydb    DATABASE     i   CREATE DATABASE skydb WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';
    DROP DATABASE skydb;
                digimon    false            3          0    21668    college 
   TABLE DATA           9   COPY public.college (id, college_name, dean) FROM stdin;
    public          digimon    false    227   u0       H          0    21783    announcement 
   TABLE DATA           R   COPY public.announcement (id, info, adate, status, college_id, title) FROM stdin;
    public          digimon    false    248   |1       (          0    21547 
   auth_group 
   TABLE DATA           .   COPY public.auth_group (id, name) FROM stdin;
    public          digimon    false    216   2       $          0    21531    django_content_type 
   TABLE DATA           C   COPY public.django_content_type (id, app_label, model) FROM stdin;
    public          digimon    false    212   22       &          0    21540    auth_permission 
   TABLE DATA           N   COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
    public          digimon    false    214   3       *          0    21556    auth_group_permissions 
   TABLE DATA           M   COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
    public          digimon    false    218   �6       ,          0    21563 	   auth_user 
   TABLE DATA           �   COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
    public          digimon    false    220   �6       .          0    21572    auth_user_groups 
   TABLE DATA           A   COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
    public          digimon    false    222   ~7       0          0    21579    auth_user_user_permissions 
   TABLE DATA           P   COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
    public          digimon    false    224   �7       5          0    21680 
   department 
   TABLE DATA           F   COPY public.department (id, name, college_id, manager_id) FROM stdin;
    public          digimon    false    229   �7       4          0    21674    course 
   TABLE DATA           P   COPY public.course (course_id, course_name, credits, department_id) FROM stdin;
    public          digimon    false    228   ,9       F          0    21769    course_requisite 
   TABLE DATA           W   COPY public.course_requisite (id, requisite_type, course_id, requisite_id) FROM stdin;
    public          digimon    false    246   �=       D          0    21761    dept_announcement 
   TABLE DATA           Z   COPY public.dept_announcement (id, info, adate, status, department_id, title) FROM stdin;
    public          digimon    false    244   �>       2          0    21638    django_admin_log 
   TABLE DATA           �   COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
    public          digimon    false    226   z?       "          0    21522    django_migrations 
   TABLE DATA           C   COPY public.django_migrations (id, app, name, applied) FROM stdin;
    public          digimon    false    210   �O       S          0    21994    django_session 
   TABLE DATA           P   COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
    public          digimon    false    259   	R       7          0    21689    login 
   TABLE DATA           T   COPY public.login (id, email, password, fname, mname, lname, user_type) FROM stdin;
    public          digimon    false    231   $S       C          0    21751    document 
   TABLE DATA           T   COPY public.document (id, name, text, qr_code, document_date, login_id) FROM stdin;
    public          digimon    false    243   8T       >          0    21724 
   instructor 
   TABLE DATA           H   COPY public.instructor (login_id, registration_id, dept_id) FROM stdin;
    public          digimon    false    238   UT       N          0    21816    program 
   TABLE DATA           W   COPY public.program (id, title, year, ptype, total_credits, department_id) FROM stdin;
    public          digimon    false    254   �T       P          0    21823    program_course 
   TABLE DATA           C   COPY public.program_course (id, program_id, course_id) FROM stdin;
    public          digimon    false    256   �T       ?          0    21731    student 
   TABLE DATA           ]   COPY public.student (login_id, sex, passed_terms, year, registration_id, status) FROM stdin;
    public          digimon    false    239   �T       R          0    21830    program_student 
   TABLE DATA           E   COPY public.program_student (id, program_id, student_id) FROM stdin;
    public          digimon    false    258   FU       9          0    21700    reaction 
   TABLE DATA           3   COPY public.reaction (id, name, emoji) FROM stdin;
    public          digimon    false    233   cU       ;          0    21707    section 
   TABLE DATA           p   COPY public.section (id, snumber, days, location, year, semester, gender, course_id, instrcutor_id) FROM stdin;
    public          digimon    false    235   �U       =          0    21716    section_announcement 
   TABLE DATA           Z   COPY public.section_announcement (id, info, adate, status, section_id, title) FROM stdin;
    public          digimon    false    237   �U       A          0    21739    section_reaction_ann 
   TABLE DATA           Z   COPY public.section_reaction_ann (id, announcement_id, login_id, reaction_id) FROM stdin;
    public          digimon    false    241   �U       L          0    21797    student_course_plan 
   TABLE DATA           _   COPY public.student_course_plan (id, year, semester, grade, course_id, student_id) FROM stdin;
    public          digimon    false    252   �U       J          0    21790    student_section 
   TABLE DATA           L   COPY public.student_section (id, grade, section_id, student_id) FROM stdin;
    public          digimon    false    250   �U       [           0    0    announcement_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.announcement_id_seq', 5, true);
          public          digimon    false    247            \           0    0    auth_group_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);
          public          digimon    false    215            ]           0    0    auth_group_permissions_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);
          public          digimon    false    217            ^           0    0    auth_permission_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.auth_permission_id_seq', 92, true);
          public          digimon    false    213            _           0    0    auth_user_groups_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);
          public          digimon    false    221            `           0    0    auth_user_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);
          public          digimon    false    219            a           0    0 !   auth_user_user_permissions_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);
          public          digimon    false    223            b           0    0    course_requisite_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.course_requisite_id_seq', 37, true);
          public          digimon    false    245            c           0    0    dept_announcement_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.dept_announcement_id_seq', 4, true);
          public          digimon    false    260            d           0    0    django_admin_log_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.django_admin_log_id_seq', 184, true);
          public          digimon    false    225            e           0    0    django_content_type_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.django_content_type_id_seq', 23, true);
          public          digimon    false    211            f           0    0    django_migrations_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.django_migrations_id_seq', 27, true);
          public          digimon    false    209            g           0    0    document_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.document_id_seq', 1, false);
          public          digimon    false    242            h           0    0    login_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.login_id_seq', 8, true);
          public          digimon    false    230            i           0    0    program_course_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.program_course_id_seq', 1, false);
          public          digimon    false    255            j           0    0    program_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.program_id_seq', 1, false);
          public          digimon    false    253            k           0    0    program_student_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.program_student_id_seq', 1, false);
          public          digimon    false    257            l           0    0    reaction_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.reaction_id_seq', 1, false);
          public          digimon    false    232            m           0    0    section_announcement_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.section_announcement_id_seq', 1, false);
          public          digimon    false    236            n           0    0    section_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.section_id_seq', 1, false);
          public          digimon    false    234            o           0    0    section_reaction_ann_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.section_reaction_ann_id_seq', 1, false);
          public          digimon    false    240            p           0    0    student_course_plan_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.student_course_plan_id_seq', 1, false);
          public          digimon    false    251            q           0    0    student_section_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.student_section_id_seq', 1, false);
          public          digimon    false    249            3   �   x�MP�n�0���Ա��j<:i�H�ta%�& K�(���P��v�#�H���7T�������i��w2��r���R`7��S
�R^D;��d�����0c`T�z��jH�0IBS�)G1�Qufa�1�u�i����M��ɥ"���kF������w���:���p���Dj�A}��J���G�=s"�r��#\y�{�^Pg�n���_Vy%�i��m�un�(^��t�2�����󱪪 p�      H   �   x��ͱ�0E�9�
���uR��܅��,ti�ą�';�����t��$f8�v�U�N�5e}-��\uT��#eH[��\ˢb���4�Ի�-��&�}��`���aWȳ������v�Bp�G$�cy{q��/�^�      (      x������ � �      $   �   x�]PA��0<�Ǭ����ً�Ԓc���u9mrcf@�Y�E�9F�웨R��G�Nt���ݹ�SHp�P�y��֙B�s"\J\��U�ޛ!�����q��I�kR���d_WQ���p�cF��JPܓ�'7=�N�M0G�z{�,<���ƍsH��ڬ� �U}�L2�RI{٨I�f����\���pҶ��L���_V�����[Ө$      &   |  x�m��Λ0���S�	� ��F�
%(��R���{�;�p�o�Y��B�}�Sw��n���?�,϶�OY����~uã$\P��Խ�R�RO�y��ٗJT�f��>+�̾p5{@�x�a'¨ϴ�C������޿�i��%+����3�!R,!��/��$ԛD�T������7������X�BWC���%ކl7�`������&���-� J�xE7 �!��y��2(Wgs����+�h#���m��R�Aޒ"U���ø��?���+����}��9�!�sA�o?�K�X)k-M�a^����S��Z�+)MDJaS��*�4�-#hi�����u�$�\I�2&���Q��78b�,��}�H�qb������ 82qk�qe{tbR1�_�NL��#�����Ĥj<2�������X�R\����{���"��a�B�U�R�u�s�qJ,��Pg3#�Rv�6A)��P�I"�Ć��=���s~.ۼ.a �eWQz�T4�AHI>��!��H�D�p�an�]�(�).専r�*�V@Hy_ �Mڟt��6�8p���_���ʮ�e�Ȣ�>�3acSI�Q�<����T5Vv�WG�%R.��Q}��kD���D����:�{S���a�����& �Z��� ��V Pޟ2����Y��ey_$��5�o��RPJ4��b)(d����)����O_�y�G*�f��J,��Mie:�F�!�̆�	���1��;+��P${�P��S�i!lJx+�o�Z��a~�]K��b!��H��@@
������qòGd���>��眿�_rm�QǴN$_x,�i��c\�����ϸ(�%+<�+E }��r ��4	! J^���s�?>�e-      *      x������ � �      ,   �   x�e�O�0@��St����[)�T(!�C�a�)�9SC��'t�]���j�e�å����O�a$�����\D�`�'��h��^�+�*�m���E�����C%�*幛``j��S�ؤ6�昢ũ,j�~^gc,�*3%�����2mbqF�[;���}��3�      .      x������ � �      0      x������ � �      5   d  x��Q�N�0<;_�/@N 9BT���^{1�IV$v�(��NJ9q�xfvv��yE=N�IC������^2V��������w����;�:�;I�j�Ѓ;oРĤ�G�N�y�꺪�Y�H�R׉�ad��l���#�m�ԯ�9�s̫P6�q����TG0t�`���J�a��vz ܒk���m��߄m����x��d�^��|(bi��d�W���K�go�NƷ�:
�@1S�A�۪,+�w����H}������o�JnD�Q����}J����A�}kF�A����|�*\�Z��G����mW�0�O ��W�¨���8�Y�aؼ0��s���ڼ��]��K�t�e����      4   �  x��V�n�6]3_�e�)$J�ci8N&�3�6i�醖i��TI�3�����%�RZ�	8����'�,Y%I��.54z&��51���I�h+�5TE����(E1ܹ��,A�����"u�D%(�Qx�}��1$z5�-L����8F^J�LUk�3�o���S�8K�GXla[��:J���3�c�sa"�:�	�=��=��m(0�y��_��|H
�F�=լ�8A�E�@Z
�4T��u��R��gj�I�5�����mM+��bY��U��7�h�%����d�إ�@4����mtm��V���0A����H��p>jި�b��"	��wz� �)�MM�	����'6�gdˇ-r�Q��X� |O�P�Yy[��!uG�a��U��X�Mu	�,г<Rnk�/T9`:ڝ	��)�КF�H?v�@ ���F�hW���gV(�(YP�����^X-ah��B��r��@o����v��ܸ-��a�ܧI�hODْ�~e�k{�n��5`���:-�]�U�`[	��������a�:�NC��!zҜ�і�g���^�V�"A�.��*HYi��G�)_��m[n�ב�C1CM�!5�)qԠ���0��d	�,+�����_ZE `0^/@��y��0{Wv2Q��S�8DbЏ��ө�4пL�-*��;���z�+�O�*%�0�m�	[G�%ue�-܍��q�%��e�-#8�Axbv/KV���F�h��o�s�g"@j?S,p��s��RȺ�E�%�m�g��J70��3\ѻ�]sK���$�4,F�o��-e  
���@j�/�x��q�g���/E%�,/�_n��Y�,�\�������`A�KϞ�v!u�o����a�>�0�_YY=��ح������7��C͐�x�yp�U��X[;�,�ϐ���� ����I붋�u6�o]}_%��I_\��vm��fN�ج�l��$�'N�p��X�{��D٧=(��,F_ԑ	;����DP�{l�W�]t ��Id+�����=�\̤� �����E?$?�w�$E�����&�9}	�x����`Z��V�6�ߣ߉b��i α�\�%Cos<�=m��G��RG�Z�@�o�/󉖷�M�}V��w)���aW@�T����@�M=��WP>�êKP���-|ck�-<�J^/����wz�	 ��|)��,_A�tww���=      F   �   x�m�A�0��� {�4�_��z
��@]���6�xl�L�ֵ�_�cy� Qg��Tp9E�:0pս�.Υ��2���0���o}`.��f,s�c�[��3�3�b�ӷ�]:�w<���s�����8�|�e�lQ      D   �   x����j�0D��W콍�W����Bs�R��m�Hk��}dRHh��e3o�nh �ΐ�݁z�̠�U��5�B�" vFwhUݘ�����g?��3�m�q��Y�N�B�.��)q��%X��i�9����}V�)ʹ�$B�i�=���Rhmm���N�5��\�ot<Fx�(]b���ʪ��m����������PR�+�Ns�      2      x��[[�E~6����ђV�/�
iH�&�Y&ZX:vg܋/C�;A��=�.�����!+P
����s�:a��g�?��"|�ؔ��A)�+�6y�Y��wm_��ow�j[u��o���}��vm�y�_���oV�n}O����٢Y߶�'���'�v9������û���������	��%�3e���Jf�J����z���_:����eL;|;OG��^$����D��矆/�BR��٧m�*�K+�ç��#�N�错�k�v����7��&D������)��
ZkŤ��?����!�? �i/ ��S�'̹d�@AlH���&Us4����mF��"c'ov�6c��uDׂgir3����K�7�e{�V�f�"�SdF�D�*�2̫�M�4���p3�{���r�a[K"���0�\��m�i�>/ek��!N�b�];�fݺ-!���Z+�}9y�������/�u��6�}�*����$��톚\-�];�^��r����_��xBז*�]ғ�����u�u��BO	�9���7��E�wMլ�����Yu��f��wE��1)�5'\h�)��oa߶��j\춻~�I��51�]���fv_B�9'�SL����]�Џ"B�d@05a�Z,䏛ͬk��N�e����$a�� G����9���%Č�fJy͘����<�o���ͪ-nu�y��!K�i�cA`��g�1�ݾ/��e�7S�k"x(�@�o���{ב]˸n�R��PKC����헻{��z�n	<�2* ��vJX-59D�7��������v*X�i8Γ�s�x|� �����1F8Gǐ_�O�R9 5�&TK�".
�0S� &��Ԛ��P��P������������{�zM5" ����4J�&!�FD�Ά���!�� r��3)��3:<SL@�LOʉ,"��& �$��H�������<���qFH�q������O��o|4�\��H$��d¿�l����0��]�3�5B3��M1�Ǉ���'�/� !��Ĉ�y"������4Ǉ�yĈ	��$��GJ\���C$�O�DIhnO�W|��#J�#+(����m�ɏ�9�)j-%.���ZXf�1X�A!'�W@Ȉ%���e��A�+�UF3��y.�QY���e�/��*��
zV���S�F�RF2�.t͹
I������X���`V�-����UFL�]��P�@���*���/�
'	"<SM���#ˌ�!�+�UFh;��BkB ���V�-��
*�0��,�U�uIP-BI�x����:%=bih�%����J<���)��Ri�U1�=�=�����h��q�#+j�*  ���\Ri�%�Ni��4邫�����յN!�T@l��;"`O�uh�
n^��D�L��46��#�w�nѮ@���s�%C���u�@��m5���e�)�y�u�l8o�X����� u�U�k�p�qo��l�İ_D{Yk��lZ����S��c����$�NB6Yv��#���� ����A�\ ����E��l7w��N���)�mca���k������]�����A�ϭ�l �ɐ,x1]�v�6�ͪL@#Rt5eKB|��DmأͲ�=�%|��k7,d��BEEIH��JɁ��`b��ާ���i���Lf��kÕ�!�q�R<�m�;�w�~�[�~7p悰�(��ʗ�)�j�/�0'�f�`���vF��k=����m ���;X�q�c��'v���2�l�f�3�ZCݥCe�N��C�,�.�.�Se��*T��}�m���Sn�pSS	쇀*61��?q=���_��r�'�گ�b��H�^0E>1Z�~)�7��w�yۯ��=�@�\�m�����	�����ە�z�
紜�8r�X\]V�䭞w�e�q�uR9<g5��� �>�y��%�T��ͽ	��O�<"�k��Jȩ����y+ti�|I\��PA*I2Kխ�l}�U�NQɕ/�=>�k�v�VW�j�XW*�?�Μ�L�Glr%���?�}�v��~�E�nJfG���������Yw�l���`�5�'�Wb����܇5?v^���m��)=B��Z�mg��?�]!#{�T��U���6!r��z���ZM܉j�����,|�!&�(��1?SMM>�?�^뿫�:���fϲ?�cE��r�k_��wK%�~~Q��E�w­'��K�����S�:����!�#:�k��o0��S�3�������Ú(c���R�3�C��̨XdRh8�%4�6sU,��.V����&�
K��*�I�� ,#��u;#���`�n������`m���C�4�h�zy�h������?�V��h���~=�d���
$r�f�W��;�U�<���`+���s�<��������REi&w�Z�T�#4�C\����]�Wc�1�s&a�彅�$C� �g���%~f�u���0"�5��	�q&\7�����Ēr�<��1�=�g*�8F��p��z��1�_�ʔ��tYӸf�ֻE��7�j�c�\C���.��J�Vo�[ ^(�����+�� �Qe\�W�U��~�n�So���3�1ͤ�}�5q�^��
�5�y�+oF�C�@�	'�~v�n3�zh��mG*B����|��-%,��*��9�+�X�SX������v�TȪ�o]A4N�T�`���ڐ�Z�}���0����l_CY�[.]/��q���Vϛ�l��o�e�x���� Shu�dq=B�Z�3���Q����4�Pꯡ/������~h
�a3}*��ǅ� �1A�Z}�ϻ5��/������ח���8�h'S���9[��I��cU�� ԛ��l\���˧��h\����]�]���s��h+S������l���a�����8��5k� ��o��;eJ7�t(l)9����������7%��a�Cݨ7������` K�e���_8�z�,�0��ݺ�D�����%�k�����]Kuv�2}۩��`J�㞩�Z]�?4��J(���F53��21����{5�$4B(��@�;PX�C˸f��Lb����d5�ʍ�h@P���,���t/R���^+ke��В���V؜u�cgw���J\@+#jn��'�2��o�w�8.RY>�ǭ��f!��u�{V�>3�s�LHzWq-8_�".^�1�*'�~����3ؑmIŊ�T�%��d���s�U��j�5�Si�?8Ј<~��Rf(RE���Pu\ы��T���S��S!��d� +��n���?BKW����~!�-����N�׀L9��=�hvMu�����q�<��M���m��gϞU㞖�`�������P�.�0x�F\$����y_�~��f���V��U�K������狲`F�f��F���!?�;5s��fdjF�V��0����-��A�h����Aaq���(��r?(��>ip���Z���ߚ��No��/�ya��ﶻͺEn���JkĲ�-�Q��~��]i �,�=n��͚Ԭvŏ�\x�|<s����'ط�}j��������h�o����'W�X��9���N���x|���`?i�MŸ��&ıR)���<��Y s�� ��)�g�~Y=6}�iȢ�+��R?��|�Y�A�u�_`�CI#��>��L�����z��7��ۡ��ä?��G��&��4�f��4���( �}+���1���v�SH2C�ܣ���]9���5�k�{�g���t��J��r$�Ć_��~���w��ޱ����r�ѭ��䨢'����_�N�Tj��JY%��P���#`5�U3o��S� �dn*�H��%���NՁ_�5���q�����L�!3�[��Ż���:���n\j��״/���Iy��&RJ��"�y��� ��%���y����� �z1�<T�~��?]�_L��h.� 3�K�vL��0���J[MJ~�.�(a���W��R@��ia*\ �e��ޜ�1V��&U�p@w�I�h�����6��wɣ��x��Z��K��v!ڿ��>��"     �R      "   g  x����n�0���S�~Ud���e%�"nj	0k�j�~mC	I����3cC�������k�cA���nr�-� �|��IMy�\����0���X�Jƒs�\���"RUI®Э�D��K�����^������"�_xeD�6��|��Zs�ͻwML��%W�%~��n�:=ѽ��1
��D�[|�M;٠:7��Q���|������!	e�r'Ԇ�5��b;�ڇ&Q嘪����t�v�0���
xBP�1��њqJɻX�����H.�ҍ"b��f�ts�:��D2�X���\�|�֝��Ø�oC�Awv�巾KI�9����a:�b�@���T�����D�O��(YQ����9E�"cĆ�zbDV�~�&�8 �=F�q����ͅg�B`|a�b�a�gÃ�B��TKU1���c��n ٭����s�2z���á^�k&JFI%��@w��l�����j���L�)؁�SnXMI�i	�bo+Jgd�?�� /@�H ��Ē�-�N���,:�R1�v�m��807z�A�D�
i%h֋��ǲ��4�m��j���s��.����LYc�����2S�b��l�������FVJ%�$���t:�r�P      S     x���n�@ ���}o0w��
Z�łE4M��(D:0�_�s2y����T��}�)�Tu��~���mE�S���`|�?�]���I�,�o�&9�l��o���_7M�/�\��3��s�����M��:���u��:�����8���wދ�5O��N��eJܹ�k��d���W8lh���%,�<��e^��2�X�e�a@�ζS	K�b���S]��k�9����%�����6a}�h��4Ք���cd�;HF���kV?@~W� ��&^�      7     x�u�Kk�0�ϫc�[�շ�
M!�^6����(�L��J2N�@��O3�)8f]��~P~	�tZB���G�Z�ͻ	��{��"�����V��m��'��ox�-W֙�sڐ<���i�
�(p�
��`�c��\�"��>�6p�~�Ѝ����1c}�H�;���F�8i�p@�,��\�{�*��?�z�h�̰�{����E6��t�lN)��Ϗ>}�ۊ��L�4���y�{8��<.|YoG�wЊp��P�3!��A&��      C      x������ � �      >   $   x�3�42404aNC.��!HĀ+F��� �g�      N      x������ � �      P      x������ � �      ?   s   x�M�1�0�Y~L!Rv�>�?������T��D�ê��F%�6[��Ͼ�K	1�ThNm����y݌hy�΋'��ŝ��|>?�ɸ�K����jm��1��R��*�      R      x������ � �      9      x������ � �      ;      x������ � �      =      x������ � �      A      x������ � �      L      x������ � �      J      x������ � �     