--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO nuages;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO nuages;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO nuages;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO nuages;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO nuages;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO nuages;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    password character varying(128) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO nuages;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO nuages;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO nuages;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO nuages;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO nuages;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO nuages;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO nuages;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO nuages;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO nuages;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO nuages;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO nuages;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO nuages;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO nuages;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: portal_apache; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_apache (
    id integer NOT NULL,
    webenvironment character varying(20) NOT NULL
);


ALTER TABLE public.portal_apache OWNER TO nuages;

--
-- Name: portal_apache_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_apache_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_apache_id_seq OWNER TO nuages;

--
-- Name: portal_apache_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_apache_id_seq OWNED BY portal_apache.id;


--
-- Name: portal_cobblerprovider; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_cobblerprovider (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    host character varying(60),
    "user" character varying(60) NOT NULL,
    password character varying(20) NOT NULL
);


ALTER TABLE public.portal_cobblerprovider OWNER TO nuages;

--
-- Name: portal_cobblerprovider_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_cobblerprovider_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_cobblerprovider_id_seq OWNER TO nuages;

--
-- Name: portal_cobblerprovider_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_cobblerprovider_id_seq OWNED BY portal_cobblerprovider.id;


--
-- Name: portal_default; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_default (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    virtualprovider_id integer NOT NULL,
    cobblerprovider_id integer NOT NULL,
    foremanprovider_id integer NOT NULL,
    consoleip inet
);


ALTER TABLE public.portal_default OWNER TO nuages;

--
-- Name: portal_default_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_default_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_default_id_seq OWNER TO nuages;

--
-- Name: portal_default_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_default_id_seq OWNED BY portal_default.id;


--
-- Name: portal_foremanprovider; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_foremanprovider (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    host character varying(60),
    port integer NOT NULL,
    "user" character varying(60),
    password character varying(20),
    mac character varying(20),
    osid character varying(20),
    envid character varying(20),
    archid character varying(20),
    puppetid character varying(20),
    ptableid character varying(20)
);


ALTER TABLE public.portal_foremanprovider OWNER TO nuages;

--
-- Name: portal_foremanprovider_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_foremanprovider_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_foremanprovider_id_seq OWNER TO nuages;

--
-- Name: portal_foremanprovider_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_foremanprovider_id_seq OWNED BY portal_foremanprovider.id;


--
-- Name: portal_ipamprovider; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_ipamprovider (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    host character varying(60) NOT NULL,
    port integer DEFAULT 80 NOT NULL,
    "user" character varying(60) NOT NULL,
    password character varying(20) NOT NULL,
    type character varying(10) DEFAULT 'nuages'::character varying NOT NULL
);


ALTER TABLE public.portal_ipamprovider OWNER TO nuages;

--
-- Name: portal_ipamprovider_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_ipamprovider_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_ipamprovider_id_seq OWNER TO nuages;

--
-- Name: portal_ipamprovider_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_ipamprovider_id_seq OWNED BY portal_ipamprovider.id;


--
-- Name: portal_ldapprovider; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_ldapprovider (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    host character varying(60),
    binddn character varying(160) NOT NULL,
    bindpassword character varying(20) NOT NULL,
    userfield character varying(60) NOT NULL,
    certname character varying(60),
    secure boolean NOT NULL,
    basedn character varying(160),
    filter character varying(160)
);


ALTER TABLE public.portal_ldapprovider OWNER TO nuages;

--
-- Name: portal_ldapprovider_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_ldapprovider_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_ldapprovider_id_seq OWNER TO nuages;

--
-- Name: portal_ldapprovider_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_ldapprovider_id_seq OWNED BY portal_ldapprovider.id;


--
-- Name: portal_oracle; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_oracle (
    id integer NOT NULL,
    sga character varying(20) NOT NULL,
    apli_size character varying(20) NOT NULL
);


ALTER TABLE public.portal_oracle OWNER TO nuages;

--
-- Name: portal_oracle_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_oracle_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_oracle_id_seq OWNER TO nuages;

--
-- Name: portal_oracle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_oracle_id_seq OWNED BY portal_oracle.id;


--
-- Name: portal_partitioning; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_partitioning (
    id integer NOT NULL,
    rootvg character varying(15) NOT NULL,
    rootsize character varying(7) NOT NULL,
    varsize character varying(7) NOT NULL,
    homesize character varying(7) NOT NULL,
    tmpsize character varying(7) NOT NULL,
    swapsize character varying(7) NOT NULL
);


ALTER TABLE public.portal_partitioning OWNER TO nuages;

--
-- Name: portal_partitioning_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_partitioning_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_partitioning_id_seq OWNER TO nuages;

--
-- Name: portal_partitioning_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_partitioning_id_seq OWNED BY portal_partitioning.id;


--
-- Name: portal_physicalprovider; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_physicalprovider (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    "user" character varying(60) NOT NULL,
    password character varying(20) NOT NULL,
    type character varying(20) DEFAULT 'ilo'::character varying NOT NULL
);


ALTER TABLE public.portal_physicalprovider OWNER TO nuages;

--
-- Name: portal_physicalprovider_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_physicalprovider_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_physicalprovider_id_seq OWNER TO nuages;

--
-- Name: portal_physicalprovider_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_physicalprovider_id_seq OWNED BY portal_physicalprovider.id;


--
-- Name: portal_profile; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_profile (
    id integer NOT NULL,
    name character varying(40) NOT NULL,
    cobblerprofile character varying(40) NOT NULL,
    clu character varying(50) NOT NULL,
    guestid character varying(20) NOT NULL,
    memory integer NOT NULL,
    numcpu integer NOT NULL,
    disksize1 integer NOT NULL,
    diskformat1 character varying(10) NOT NULL,
    disksize2 integer,
    diskformat2 character varying(10) NOT NULL,
    numinterfaces integer NOT NULL,
    net1 character varying(10) NOT NULL,
    subnet1 inet,
    net2 character varying(10) NOT NULL,
    subnet2 inet,
    net3 character varying(10) NOT NULL,
    subnet3 inet,
    net4 character varying(10) NOT NULL,
    subnet4 inet,
    diskinterface character varying(20) NOT NULL,
    netinterface character varying(20) NOT NULL,
    cmdline character varying(100) NOT NULL,
    dns character varying(20),
    foreman boolean NOT NULL,
    cobbler boolean NOT NULL,
    iso boolean NOT NULL,
    partitioning boolean NOT NULL,
    datacenter character varying(50) NOT NULL,
    autostorage boolean NOT NULL,
    physicalprovider_id integer,
    virtualprovider_id integer,
    cobblerprovider_id integer,
    foremanprovider_id integer,
    hide boolean NOT NULL,
    console boolean NOT NULL,
    ipamprovider_id integer,
    requireip boolean NOT NULL
);


ALTER TABLE public.portal_profile OWNER TO nuages;

--
-- Name: portal_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_profile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_profile_id_seq OWNER TO nuages;

--
-- Name: portal_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_profile_id_seq OWNED BY portal_profile.id;


--
-- Name: portal_rac; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_rac (
    id integer NOT NULL,
    racvip inet NOT NULL,
    racversion character varying(4) NOT NULL,
    racnodes integer NOT NULL,
    racasm character varying(2) DEFAULT 'NO'::character varying NOT NULL
);


ALTER TABLE public.portal_rac OWNER TO nuages;

--
-- Name: portal_rac_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_rac_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_rac_id_seq OWNER TO nuages;

--
-- Name: portal_rac_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_rac_id_seq OWNED BY portal_rac.id;


--
-- Name: portal_sap; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_sap (
    id integer NOT NULL,
    sapsid integer NOT NULL,
    saptier character varying(3) NOT NULL
);


ALTER TABLE public.portal_sap OWNER TO nuages;

--
-- Name: portal_sap_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_sap_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_sap_id_seq OWNER TO nuages;

--
-- Name: portal_sap_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_sap_id_seq OWNED BY portal_sap.id;


--
-- Name: portal_storage; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_storage (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    type character varying(20) NOT NULL,
    provider_id integer NOT NULL,
    datacenter character varying(50) NOT NULL
);


ALTER TABLE public.portal_storage OWNER TO nuages;

--
-- Name: portal_storage_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_storage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_storage_id_seq OWNER TO nuages;

--
-- Name: portal_storage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_storage_id_seq OWNED BY portal_storage.id;


--
-- Name: portal_type; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_type (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    parameters text NOT NULL
);


ALTER TABLE public.portal_type OWNER TO nuages;

--
-- Name: portal_type_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_type_id_seq OWNER TO nuages;

--
-- Name: portal_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_type_id_seq OWNED BY portal_type.id;


--
-- Name: portal_virtualprovider; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_virtualprovider (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    host character varying(60),
    port integer NOT NULL,
    "user" character varying(60) NOT NULL,
    password character varying(20) NOT NULL,
    type character varying(20) NOT NULL,
    ssl boolean NOT NULL,
    clu character varying(50) NOT NULL,
    datacenter character varying(50) NOT NULL,
    active boolean NOT NULL
);


ALTER TABLE public.portal_virtualprovider OWNER TO nuages;

--
-- Name: portal_virtualprovider_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_virtualprovider_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_virtualprovider_id_seq OWNER TO nuages;

--
-- Name: portal_virtualprovider_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_virtualprovider_id_seq OWNED BY portal_virtualprovider.id;


--
-- Name: portal_vm; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_vm (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    virtualprovider_id integer,
    cobblerprovider_id integer,
    foremanprovider_id integer,
    profile_id integer NOT NULL,
    ip1 inet,
    mac1 character varying(20),
    ip2 inet,
    mac2 character varying(20),
    ip3 inet,
    mac3 character varying(20),
    ip4 inet,
    mac4 character varying(20),
    ipilo inet,
    iso character varying(30) NOT NULL,
    hostgroup character varying(30) NOT NULL,
    puppetclasses text NOT NULL,
    puppetparameters text NOT NULL,
    cobblerparameters text NOT NULL,
    createdby_id integer NOT NULL,
    status character varying(20) NOT NULL,
    storagedomain character varying(60),
    physicalprovider_id integer,
    physical boolean NOT NULL,
    type_id integer
);


ALTER TABLE public.portal_vm OWNER TO nuages;

--
-- Name: portal_vm_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_vm_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_vm_id_seq OWNER TO nuages;

--
-- Name: portal_vm_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_vm_id_seq OWNED BY portal_vm.id;


--
-- Name: portal_weblogic; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE portal_weblogic (
    id integer NOT NULL,
    wlversion character varying(5) DEFAULT '1036'::character varying NOT NULL,
    wlsizeapli character varying(5) DEFAULT '5120'::character varying NOT NULL,
    wlsizeapp character varying(5) DEFAULT '2048'::character varying NOT NULL,
    wlsizelog character varying(5) DEFAULT '2048'::character varying NOT NULL
);


ALTER TABLE public.portal_weblogic OWNER TO nuages;

--
-- Name: portal_weblogic_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE portal_weblogic_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.portal_weblogic_id_seq OWNER TO nuages;

--
-- Name: portal_weblogic_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE portal_weblogic_id_seq OWNED BY portal_weblogic.id;


--
-- Name: south_migrationhistory; Type: TABLE; Schema: public; Owner: nuages; Tablespace: 
--

CREATE TABLE south_migrationhistory (
    id integer NOT NULL,
    app_name character varying(255) NOT NULL,
    migration character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.south_migrationhistory OWNER TO nuages;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: nuages
--

CREATE SEQUENCE south_migrationhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.south_migrationhistory_id_seq OWNER TO nuages;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nuages
--

ALTER SEQUENCE south_migrationhistory_id_seq OWNED BY south_migrationhistory.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_apache ALTER COLUMN id SET DEFAULT nextval('portal_apache_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_cobblerprovider ALTER COLUMN id SET DEFAULT nextval('portal_cobblerprovider_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_default ALTER COLUMN id SET DEFAULT nextval('portal_default_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_foremanprovider ALTER COLUMN id SET DEFAULT nextval('portal_foremanprovider_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_ipamprovider ALTER COLUMN id SET DEFAULT nextval('portal_ipamprovider_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_ldapprovider ALTER COLUMN id SET DEFAULT nextval('portal_ldapprovider_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_oracle ALTER COLUMN id SET DEFAULT nextval('portal_oracle_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_partitioning ALTER COLUMN id SET DEFAULT nextval('portal_partitioning_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_physicalprovider ALTER COLUMN id SET DEFAULT nextval('portal_physicalprovider_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_profile ALTER COLUMN id SET DEFAULT nextval('portal_profile_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_rac ALTER COLUMN id SET DEFAULT nextval('portal_rac_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_sap ALTER COLUMN id SET DEFAULT nextval('portal_sap_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_storage ALTER COLUMN id SET DEFAULT nextval('portal_storage_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_type ALTER COLUMN id SET DEFAULT nextval('portal_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_virtualprovider ALTER COLUMN id SET DEFAULT nextval('portal_virtualprovider_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_vm ALTER COLUMN id SET DEFAULT nextval('portal_vm_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_weblogic ALTER COLUMN id SET DEFAULT nextval('portal_weblogic_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY south_migrationhistory ALTER COLUMN id SET DEFAULT nextval('south_migrationhistory_id_seq'::regclass);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_key; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_key; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_key; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_key; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_key; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_key UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: portal_apache_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_apache
    ADD CONSTRAINT portal_apache_pkey PRIMARY KEY (id);


--
-- Name: portal_cobblerprovider_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_cobblerprovider
    ADD CONSTRAINT portal_cobblerprovider_pkey PRIMARY KEY (id);


--
-- Name: portal_default_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_default
    ADD CONSTRAINT portal_default_pkey PRIMARY KEY (id);


--
-- Name: portal_foremanprovider_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_foremanprovider
    ADD CONSTRAINT portal_foremanprovider_pkey PRIMARY KEY (id);


--
-- Name: portal_ipamprovider_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_ipamprovider
    ADD CONSTRAINT portal_ipamprovider_pkey PRIMARY KEY (id);


--
-- Name: portal_ldapprovider_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_ldapprovider
    ADD CONSTRAINT portal_ldapprovider_pkey PRIMARY KEY (id);


--
-- Name: portal_oracle_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_oracle
    ADD CONSTRAINT portal_oracle_pkey PRIMARY KEY (id);


--
-- Name: portal_partitioning_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_partitioning
    ADD CONSTRAINT portal_partitioning_pkey PRIMARY KEY (id);


--
-- Name: portal_physicalprovider_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_physicalprovider
    ADD CONSTRAINT portal_physicalprovider_pkey PRIMARY KEY (id);


--
-- Name: portal_profile_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_profile
    ADD CONSTRAINT portal_profile_pkey PRIMARY KEY (id);


--
-- Name: portal_rac_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_rac
    ADD CONSTRAINT portal_rac_pkey PRIMARY KEY (id);


--
-- Name: portal_sap_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_sap
    ADD CONSTRAINT portal_sap_pkey PRIMARY KEY (id);


--
-- Name: portal_storage_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_storage
    ADD CONSTRAINT portal_storage_pkey PRIMARY KEY (id);


--
-- Name: portal_type_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_type
    ADD CONSTRAINT portal_type_pkey PRIMARY KEY (id);


--
-- Name: portal_virtualprovider_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_virtualprovider
    ADD CONSTRAINT portal_virtualprovider_pkey PRIMARY KEY (id);


--
-- Name: portal_vm_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_vm
    ADD CONSTRAINT portal_vm_pkey PRIMARY KEY (id);


--
-- Name: portal_weblogic_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY portal_weblogic
    ADD CONSTRAINT portal_weblogic_pkey PRIMARY KEY (id);


--
-- Name: south_migrationhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: nuages; Tablespace: 
--

ALTER TABLE ONLY south_migrationhistory
    ADD CONSTRAINT south_migrationhistory_pkey PRIMARY KEY (id);


--
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX django_session_expire_date ON django_session USING btree (expire_date);


--
-- Name: portal_default_cobblerprovider_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_default_cobblerprovider_id ON portal_default USING btree (cobblerprovider_id);


--
-- Name: portal_default_foremanprovider_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_default_foremanprovider_id ON portal_default USING btree (foremanprovider_id);


--
-- Name: portal_default_virtualprovider_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_default_virtualprovider_id ON portal_default USING btree (virtualprovider_id);


--
-- Name: portal_profile_cobblerprovider_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_profile_cobblerprovider_id ON portal_profile USING btree (cobblerprovider_id);


--
-- Name: portal_profile_foremanprovider_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_profile_foremanprovider_id ON portal_profile USING btree (foremanprovider_id);


--
-- Name: portal_profile_ipamprovider_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_profile_ipamprovider_id ON portal_profile USING btree (ipamprovider_id);


--
-- Name: portal_profile_physicalprovider_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_profile_physicalprovider_id ON portal_profile USING btree (physicalprovider_id);


--
-- Name: portal_profile_virtualprovider_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_profile_virtualprovider_id ON portal_profile USING btree (virtualprovider_id);


--
-- Name: portal_storage_provider_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_storage_provider_id ON portal_storage USING btree (provider_id);


--
-- Name: portal_vm_cobblerprovider_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_vm_cobblerprovider_id ON portal_vm USING btree (cobblerprovider_id);


--
-- Name: portal_vm_createdby_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_vm_createdby_id ON portal_vm USING btree (createdby_id);


--
-- Name: portal_vm_foremanprovider_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_vm_foremanprovider_id ON portal_vm USING btree (foremanprovider_id);


--
-- Name: portal_vm_physicalprovider_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_vm_physicalprovider_id ON portal_vm USING btree (physicalprovider_id);


--
-- Name: portal_vm_profile_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_vm_profile_id ON portal_vm USING btree (profile_id);


--
-- Name: portal_vm_type_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_vm_type_id ON portal_vm USING btree (type_id);


--
-- Name: portal_vm_virtualprovider_id; Type: INDEX; Schema: public; Owner: nuages; Tablespace: 
--

CREATE INDEX portal_vm_virtualprovider_id ON portal_vm USING btree (virtualprovider_id);


--
-- Name: auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cobblerprovider_id_refs_id_25994c0caf7a7c2b; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_vm
    ADD CONSTRAINT cobblerprovider_id_refs_id_25994c0caf7a7c2b FOREIGN KEY (cobblerprovider_id) REFERENCES portal_cobblerprovider(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cobblerprovider_id_refs_id_284343fb5526a0e; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_profile
    ADD CONSTRAINT cobblerprovider_id_refs_id_284343fb5526a0e FOREIGN KEY (cobblerprovider_id) REFERENCES portal_cobblerprovider(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_728de91f; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_728de91f FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: foremanprovider_id_refs_id_2086a564551b997f; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_profile
    ADD CONSTRAINT foremanprovider_id_refs_id_2086a564551b997f FOREIGN KEY (foremanprovider_id) REFERENCES portal_foremanprovider(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: foremanprovider_id_refs_id_36bef6d036085138; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_vm
    ADD CONSTRAINT foremanprovider_id_refs_id_36bef6d036085138 FOREIGN KEY (foremanprovider_id) REFERENCES portal_foremanprovider(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: group_id_refs_id_3cea63fe; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT group_id_refs_id_3cea63fe FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ipamprovider_id_refs_id_6bc196618e95f61; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_profile
    ADD CONSTRAINT ipamprovider_id_refs_id_6bc196618e95f61 FOREIGN KEY (ipamprovider_id) REFERENCES portal_ipamprovider(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: physicalprovider_id_refs_id_4b9a4f1127661dce; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_vm
    ADD CONSTRAINT physicalprovider_id_refs_id_4b9a4f1127661dce FOREIGN KEY (physicalprovider_id) REFERENCES portal_physicalprovider(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: physicalprovider_id_refs_id_62e6e7cf52c099eb; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_profile
    ADD CONSTRAINT physicalprovider_id_refs_id_62e6e7cf52c099eb FOREIGN KEY (physicalprovider_id) REFERENCES portal_physicalprovider(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: portal_default_cobblerprovider_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_default
    ADD CONSTRAINT portal_default_cobblerprovider_id_fkey FOREIGN KEY (cobblerprovider_id) REFERENCES portal_cobblerprovider(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: portal_default_foremanprovider_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_default
    ADD CONSTRAINT portal_default_foremanprovider_id_fkey FOREIGN KEY (foremanprovider_id) REFERENCES portal_foremanprovider(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: portal_default_virtualprovider_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_default
    ADD CONSTRAINT portal_default_virtualprovider_id_fkey FOREIGN KEY (virtualprovider_id) REFERENCES portal_virtualprovider(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: portal_vm_createdby_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_vm
    ADD CONSTRAINT portal_vm_createdby_id_fkey FOREIGN KEY (createdby_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: portal_vm_profile_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_vm
    ADD CONSTRAINT portal_vm_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES portal_profile(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: provider_id_refs_id_6871f0c196ca5c4c; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_storage
    ADD CONSTRAINT provider_id_refs_id_6871f0c196ca5c4c FOREIGN KEY (provider_id) REFERENCES portal_virtualprovider(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: type_id_refs_id_5023027f7eaaffd6; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_vm
    ADD CONSTRAINT type_id_refs_id_5023027f7eaaffd6 FOREIGN KEY (type_id) REFERENCES portal_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_831107f1; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT user_id_refs_id_831107f1 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_f2045483; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT user_id_refs_id_f2045483 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: virtualprovider_id_refs_id_51852074191c78d8; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_profile
    ADD CONSTRAINT virtualprovider_id_refs_id_51852074191c78d8 FOREIGN KEY (virtualprovider_id) REFERENCES portal_virtualprovider(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: virtualprovider_id_refs_id_a376701db8a6bd1; Type: FK CONSTRAINT; Schema: public; Owner: nuages
--

ALTER TABLE ONLY portal_vm
    ADD CONSTRAINT virtualprovider_id_refs_id_a376701db8a6bd1 FOREIGN KEY (virtualprovider_id) REFERENCES portal_virtualprovider(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

