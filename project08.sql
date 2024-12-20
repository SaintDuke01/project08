PGDMP                  
    |         	   project_8    16.4 (Debian 16.4-1.pgdg120+2)    16.4 "    B           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            C           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            D           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            E           1262    16558 	   project_8    DATABASE     t   CREATE DATABASE project_8 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
    DROP DATABASE project_8;
             	   project_8    false            F           0    0    DATABASE project_8    ACL     <   REVOKE CONNECT,TEMPORARY ON DATABASE project_8 FROM PUBLIC;
                	   project_8    false    3397            �            1255    17013    set_member_mid()    FUNCTION     �   CREATE FUNCTION public.set_member_mid() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.MID IS NULL THEN
        NEW.MID := NEXTVAL('MEMBER_MID_SEQ');
    END IF;
    RETURN NEW;
END;
$$;
 '   DROP FUNCTION public.set_member_mid();
       public       	   project_8    false            �            1255    17015    set_order_oid()    FUNCTION     �   CREATE FUNCTION public.set_order_oid() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.OID IS NULL THEN
        NEW.OID := NEXTVAL('ORDER_OID_SEQ');
    END IF;
    RETURN NEW;
END;
$$;
 &   DROP FUNCTION public.set_order_oid();
       public       	   project_8    false            �            1259    19282    book_id    TABLE     �   CREATE TABLE public.book_id (
    book_id integer NOT NULL,
    serialnumber integer NOT NULL,
    location character varying(50),
    addtime timestamp without time zone,
    callnumber character varying(50)
);
    DROP TABLE public.book_id;
       public         heap 	   project_8    false            �            1259    19312    book_review    TABLE     �   CREATE TABLE public.book_review (
    name character varying(50),
    description text,
    score integer,
    callnumber character varying(50),
    id integer,
    CONSTRAINT book_review_score_check CHECK (((score >= 0) AND (score <= 10)))
);
    DROP TABLE public.book_review;
       public         heap 	   project_8    false            �            1259    19275 
   book_title    TABLE     �   CREATE TABLE public.book_title (
    callnumber character varying(50) NOT NULL,
    content text,
    name character varying(100),
    author character varying(50)
);
    DROP TABLE public.book_title;
       public         heap 	   project_8    false            �            1259    19483    borrow_log_serialnumber_seq    SEQUENCE     �   CREATE SEQUENCE public.borrow_log_serialnumber_seq
    START WITH 21
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.borrow_log_serialnumber_seq;
       public       	   project_8    false            �            1259    19297 
   borrow_log    TABLE     �   CREATE TABLE public.borrow_log (
    sn integer DEFAULT nextval('public.borrow_log_serialnumber_seq'::regclass) NOT NULL,
    borrowdatetime timestamp without time zone,
    id integer,
    book_id integer,
    serialnumber integer NOT NULL
);
    DROP TABLE public.borrow_log;
       public         heap 	   project_8    false    224            �            1259    16990    cart_tno_seq    SEQUENCE     v   CREATE SEQUENCE public.cart_tno_seq
    START WITH 9
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 20;
 #   DROP SEQUENCE public.cart_tno_seq;
       public       	   project_8    false            �            1259    16991    member_mid_seq    SEQUENCE     x   CREATE SEQUENCE public.member_mid_seq
    START WITH 5
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 20;
 %   DROP SEQUENCE public.member_mid_seq;
       public       	   project_8    false            �            1259    16992    order_oid_seq    SEQUENCE     w   CREATE SEQUENCE public.order_oid_seq
    START WITH 9
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 20;
 $   DROP SEQUENCE public.order_oid_seq;
       public       	   project_8    false            �            1259    19405    userinformation_id_seq    SEQUENCE        CREATE SEQUENCE public.userinformation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.userinformation_id_seq;
       public       	   project_8    false            �            1259    19292    userinformation    TABLE       CREATE TABLE public.userinformation (
    username character varying(50),
    permission character varying(20),
    password character varying(50),
    email character varying(100),
    id integer DEFAULT nextval('public.userinformation_id_seq'::regclass) NOT NULL
);
 #   DROP TABLE public.userinformation;
       public         heap 	   project_8    false    223            :          0    19282    book_id 
   TABLE DATA           W   COPY public.book_id (book_id, serialnumber, location, addtime, callnumber) FROM stdin;
    public       	   project_8    false    219   �'       =          0    19312    book_review 
   TABLE DATA           O   COPY public.book_review (name, description, score, callnumber, id) FROM stdin;
    public       	   project_8    false    222   s(       9          0    19275 
   book_title 
   TABLE DATA           G   COPY public.book_title (callnumber, content, name, author) FROM stdin;
    public       	   project_8    false    218   +       <          0    19297 
   borrow_log 
   TABLE DATA           S   COPY public.borrow_log (sn, borrowdatetime, id, book_id, serialnumber) FROM stdin;
    public       	   project_8    false    221   <.       ;          0    19292    userinformation 
   TABLE DATA           T   COPY public.userinformation (username, permission, password, email, id) FROM stdin;
    public       	   project_8    false    220   �/       G           0    0    borrow_log_serialnumber_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.borrow_log_serialnumber_seq', 53, true);
          public       	   project_8    false    224            H           0    0    cart_tno_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.cart_tno_seq', 68, true);
          public       	   project_8    false    215            I           0    0    member_mid_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.member_mid_seq', 224, true);
          public       	   project_8    false    216            J           0    0    order_oid_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.order_oid_seq', 28, true);
          public       	   project_8    false    217            K           0    0    userinformation_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.userinformation_id_seq', 35, true);
          public       	   project_8    false    223            �           2606    19286    book_id book_id_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.book_id
    ADD CONSTRAINT book_id_pkey PRIMARY KEY (book_id, serialnumber);
 >   ALTER TABLE ONLY public.book_id DROP CONSTRAINT book_id_pkey;
       public         	   project_8    false    219    219            �           2606    19281    book_title book_title_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.book_title
    ADD CONSTRAINT book_title_pkey PRIMARY KEY (callnumber);
 D   ALTER TABLE ONLY public.book_title DROP CONSTRAINT book_title_pkey;
       public         	   project_8    false    218            �           2606    19301    borrow_log borrow_log_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.borrow_log
    ADD CONSTRAINT borrow_log_pkey PRIMARY KEY (sn);
 D   ALTER TABLE ONLY public.borrow_log DROP CONSTRAINT borrow_log_pkey;
       public         	   project_8    false    221            �           2606    19408 $   userinformation userinformation_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.userinformation
    ADD CONSTRAINT userinformation_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.userinformation DROP CONSTRAINT userinformation_pkey;
       public         	   project_8    false    220            �           2606    19287    book_id book_id_callnumber_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.book_id
    ADD CONSTRAINT book_id_callnumber_fkey FOREIGN KEY (callnumber) REFERENCES public.book_title(callnumber);
 I   ALTER TABLE ONLY public.book_id DROP CONSTRAINT book_id_callnumber_fkey;
       public       	   project_8    false    218    219    3229            �           2606    19318 '   book_review book_review_callnumber_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.book_review
    ADD CONSTRAINT book_review_callnumber_fkey FOREIGN KEY (callnumber) REFERENCES public.book_title(callnumber);
 Q   ALTER TABLE ONLY public.book_review DROP CONSTRAINT book_review_callnumber_fkey;
       public       	   project_8    false    218    3229    222            �           2606    19307 /   borrow_log borrow_log_book_id_serialnumber_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.borrow_log
    ADD CONSTRAINT borrow_log_book_id_serialnumber_fkey FOREIGN KEY (book_id, serialnumber) REFERENCES public.book_id(book_id, serialnumber);
 Y   ALTER TABLE ONLY public.borrow_log DROP CONSTRAINT borrow_log_book_id_serialnumber_fkey;
       public       	   project_8    false    221    219    221    3231    219            :   �   x��ѹBQD��M4 򼿓��;!�!Q�"� ";	�ᑃ�LL����x�F)[.����hC�]�L����X����D����R%*W3�*Ԯ�J�h\-�jкZ*բs�R���Z0Hgž���[�2��)V�!�^��U`HpT�C��b"�k�P�X�*\ˆ� ����,      =   �  x�]��V�@���O1O0�p�Ι��g1	�K ��-����hP�(�<�����W��3����������0�a���_�s=��vl6����՛Z"E�%�J�4e�l,�*�F�q��A��v-��$��P�d(��P��s��/ΰ�+M��QrU�E�H��^�VRϒ,��,�5�Oh^������:n���#��$r$Gò��^��7b.>jH��쟘�S�����q<�9�|��C�MhM���
vM	���OEc>3���$O�����;=�ߊC[������;x툨D%�W ʭ�@���H�]�9�Z��+f͒؋�H�*�M���=�N�ו-����v�����ػ��VJ�HQI��5��Ӑ]���HJ��SI@�(
ŋ� �5�rGMgw*[�q]���ō���~L�����`�F���o]&�Df]2K��	�50���V"�Q2�5�A.P�o��Ո)�Ma����hBMF8�'�d���3J@#��|?�X��J�}�#a	�*��0G���MxH�L\Hɂlf;�x}6.?aM�SQ�n�7Q{d�Arq���7�ˠcF���t&.($��9��E�����_�'!��RL
�b\)*����>�j�m}�Oc�ϔ�߸4(�      9     x�u�[RA���Ud���\^}I�� #20^����C�3��Un%sNw�"�P&<䅂������a/�����5?��������w&+�E5k�z$�`N�C�M_��jj/������"���O�5:�ي��sBV`da�Po��� ��I�������᫹x��z���!�>�zE ֭�g�k��'4>6M�497׮��߰��u^�3�:�*�he2יw�4��`���y#�q��r�Tdߍ�����Hw�'ta>	>�B�)�h�n��Yr�29�}���;��7|T���]��Q�,���N�¬Pwi��IUf�0_�<>T�n�Xh��^}�Z�~{���GEZTjRwd��A��r���F:s�����ό�\�u���@����gznRh4��B�|��e�Z��ޅ��`�\��{�6�I*�`�ű��B<�'�'�n��k�G�����m�E4ͫ��>���7C"�tY	*��ʭ�H|@23?���ͤn��M�^׳Lΰ��|+�7��*�^��ՐϚ�/�t����:
'���|S��B���Wn��q4]+�
S�˩���i���6C�����g������N3t�����xe�۲լ'�нO���y=Xؒ�j����u�'�Ȏ��%�YO|A�W��xq�3M.f(�[����T�?J�Q#q��W��V�%������e��� �eO�9x���	T>�$v���{��@�v�Ĩ��`x����8t(�a��b#g�4��w�L�d�[�T��m9      <   �  x�u��q�0Eϫ*��f�ɲkI�u��%٬����xH{6<[�臶��<�$� &�[2M�U�3e�X�Ya��'�k����bhX�ʖ��â���2�I��:'eO�c��3P��7/g��S����o�������^v�z�~��]~����0�����"�#����.	iIZVEG�	�I�Uђ�B�ɪ��U!]�fU4�$e�eU���:�@P��|h;�o��#��cm�ݗ��{�j��������e��ő��1��f�3��yGcI����ʵ��ʕki̷Ab8_��������s;}���,Ka�
^$1�����'tR����*�T�~��@lKY>؜�xdF���S{ʒ����Joط���wyÈ;&�h$��|�R~ *b�3      ;   �  x���MO�@�ϝo� ;��rRQ��dBbf�����`�㲜 +�(4$JȚp#!�� ��e�+�-��vaN^�i�<�?��f��������eNEQ�'���x~�䴢�d�9YHx� �w�����)��D��(v��a�]p���97�.�.	��B�:��9���?�N.GF�d�̩��J��q����ٛ�z���W1��ON�T�͌���-} �O�M~����)�	�Wq6D�rK�����m�/)g�~BT���2;H�O�vr��lcJx���j��$�BhYb0��VY��̄3��%��T�JƇ�r���}�Sv����Lm����b][���g�Wp��'r�pF*��A�v P�P�5\�Lա/�B�6��~��F����!T��0l�'�}�%���I���9)5h.`h���4g-5��>HR��)>G-���H��myfG���m�%r�o��Ա-�Ba,��"	܂�l�0��G��E>�%ߓ+d�F0�v�JG�\!6��^���.��&�\Nd�F�~��L�L4��w���#ͼ�t�]W�|���f�<ţ�2���A����|0�ܞn��F��s8ˇ��"���ܨC����U�gϗSE����=�謗�G���H)��(�����zH�끕 �?�� �     