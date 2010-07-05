-- MySQL dump 10.13  Distrib 5.1.37, for debian-linux-gnu (i486)
--
-- Host: localhost    Database: bioport_test
-- ------------------------------------------------------
-- Server version	5.1.37-1ubuntu5.4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `antiidentical`
--

DROP TABLE IF EXISTS `antiidentical`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `antiidentical` (
  `bioport_id1` varchar(50) NOT NULL,
  `bioport_id2` varchar(50) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`bioport_id1`,`bioport_id2`),
  KEY `bioport_id2` (`bioport_id2`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `antiidentical`
--

LOCK TABLES `antiidentical` WRITE;
/*!40000 ALTER TABLE `antiidentical` DISABLE KEYS */;
/*!40000 ALTER TABLE `antiidentical` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `author`
--

DROP TABLE IF EXISTS `author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `author`
--

LOCK TABLES `author` WRITE;
/*!40000 ALTER TABLE `author` DISABLE KEYS */;
/*!40000 ALTER TABLE `author` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `biography`
--

DROP TABLE IF EXISTS `biography`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `biography` (
  `id` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `source_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `biodes_document` text,
  `source_url` varchar(255) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `hide` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_biography_id` (`id`),
  KEY `ix_biography_source_id` (`source_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biography`
--

LOCK TABLES `biography` WRITE;
/*!40000 ALTER TABLE `biography` DISABLE KEYS */;
INSERT INTO `biography` VALUES ('knaw/001','knaw','<biodes version=\"1.0\">\n  <fileDesc>\n    <title/>\n    <author>Brongersma, L.D.</author>\n    <author>Brongersma, L.D.</author>\n    <author>Jongkees, L.B.W.</author>\n    <ref target=\"http://www.digitallibrary.nl/levensberichten/authors_detail.cfm?RecordId=237\"/>\n    <publisher>\n      <name>KNAW - Levensberichten en Herdenkingen</name>\n      <ref target=\"http://www.digitallibrary.nl/levensberichten/works.cfm\"/>\n    </publisher>\n  </fileDesc>\n  <person>\n    <idno type=\"id\">001</idno>\n    <persName><name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma</name></persName>\n    <sex value=\"1\"/>\n    <event type=\"birth\" when=\"1893-04-22\">\n      <place>IJsbrechtum</place>\n    </event>\n    <event type=\"death\" when=\"1976-07-22\">\n      <place>Leiden</place>\n    </event>\n    <state type=\"occupation\">Biologie</state>\n    <state type=\"occupation\">Zo&#246;logie</state>\n  <idno type=\"bioport\">27201748</idno></person>\n  <biography>\n	  <graphic url=\"../images/image1.jpg\"/>\n	  <graphic url=\"../images/im&#235;ge.jpg\"/>\n  	  <graphic url=\"../images2/image1.jpg\"/>\n	 <graphic url=\"http://www.knaw.nl/cfdata/leden/images/Micha&#235;lis_NTh_545.jpg\"/>\n  </biography>\n</biodes>\n','file:///home/jelle/projects_active/bioport/site/parts/Products/BioPortRepository/tests/data/knaw/001.xml','2010-06-11 08:42:37',NULL),('knaw/002','knaw','<biodes version=\"1.0\">\n  <fileDesc>\n    <title/>\n    <author>Vrolik, W.</author>\n    <ref target=\"http://www.digitallibrary.nl/levensberichten/authors_detail.cfm?RecordId=1801\"/>\n    <publisher>\n      <name>KNAW - Levensberichten en Herdenkingen</name>\n      <ref target=\"http://www.digitallibrary.nl/levensberichten/works.cfm\"/>\n    </publisher>\n  </fileDesc>\n  <person>\n    <idno type=\"id\">002</idno>\n    <persName><name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma twee</name></persName>\n    <sex value=\"1\"/>\n    <event type=\"birth\" when=\"1778-03-31\">\n      <place>Amsterdam</place>\n    </event>\n    <event type=\"death\" when=\"1858-01-30\">\n      <place>Lisse</place>\n    </event>\n    <state type=\"occupation\">Ornitologie</state>\n    <state type=\"occupation\">Zo&#246;logie</state>\n    <state type=\"category\" idno=\"1\">category 1</state>\n  <idno type=\"bioport\">84972544</idno></person>\n  <biography>\n  <text>Dit is een test-tekst. Dit woord Molloy staat alleen in de tekst.</text>\n  </biography>\n</biodes>\n','file:///home/jelle/projects_active/bioport/site/parts/Products/BioPortRepository/tests/data/knaw/002.xml','2010-06-11 08:42:37',NULL),('knaw/003','knaw','<biodes version=\"1.0\">\n  <fileDesc>\n    <title/>\n    <author>Visser - \'t Hooft, W.A.</author>\n    <ref target=\"http://www.digitallibrary.nl/levensberichten/authors_detail.cfm?RecordId=1046\"/>\n    <publisher>\n      <name>KNAW - Levensberichten en Herdenkingen</name>\n      <ref target=\"http://www.digitallibrary.nl/levensberichten/works.cfm\"/>\n    </publisher>\n  </fileDesc>\n  <person>\n    <idno type=\"id\">003</idno>\n    <persName>\n        <name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma</name>\n        <name type=\"voornaam\">Hendrik</name> <name type=\"geslachtsnaam\">Kraemer</name>\n    </persName>\n    <sex value=\"1\"/>\n    <event type=\"birth\" when=\"1888-05-17\">\n      <place>Amsterdam</place>\n    </event>\n    <event type=\"death\" when=\"1965-11-11\">\n      <place>Driebergen</place>\n    </event>\n    <state type=\"occupation\">Theologie</state>\n    <state type=\"occupation\">Zendingswetenschappen</state>\n  <idno type=\"bioport\">44333513</idno></person>\n <biography>\n    <graphic url=\"../images/image2.jpg\"/>\n    <text>&lt;html&gt;&lt;head&gt;&lt;meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"&gt;&lt;link rel=\"stylesheet\" type=\"text/css\" href=\"stylesheet\"&gt;&lt;/head&gt;&lt;body bottommargin=\"15\" leftmargin=\"10\" topmargin=\"15\" rightmargin=\"10\"&gt;&lt;p&gt;&lt;b&gt;POPPES, Eelkje &lt;/b&gt;(geb. Lemmer, Friesland, 9-2-1791 &#8211; gest. Leeuwarden 20-9-1828), gelegenheidsdichteres. Dochter van Poppe Jans Poppes (1747-1810) en Antje Annes Visser (1758-1832). Op 22-6-1815 trouwde Eelkje Poppes in Lemmer met &lt;b&gt;Christianus Petrus Eliza Robid&#233; van der Aa&lt;/b&gt; (1791-1851), advocaat, letterkundige, dichter. Uit het huwelijk werden 8 kinderen geboren, van wie 3 dochters de volwassen leeftijd bereikten. Er was wellicht ook 1 pleegzoon.&lt;/p&gt;&lt;p&gt;&lt;img class=\"dvn\" src=\"plaatjes/EelkjePoppes.jpg\"/&gt;Eelkje Poppes stamde uit een &#8216;achtenswaardig&#8217; (Van der Aa) Fries geslacht. In 1814 verscheen van haar, autodidact in de dichtkunst, een bundeltje van drie gedichten onder de titel: &lt;i&gt;Eerstelingen aan mijn vaderland&lt;/i&gt;, voorafgegaan door een lofdicht van haar toekomstige man. Deze patriottisch-orangistische verzen schreef zij naar aanleiding van de val van Napoleon en het vertrek van de Fransen uit Nederland eind 1813.&lt;/p&gt;&lt;p&gt;In 1815 trouwde zij met Christianus Robid&#233; van der Aa, die toen secretaris van Lemsterland was. Het echtpaar ging in 1818 in Leeuwarden wonen en betrok daar wat tegenwoordig het Fries Letterkundig Museum en Documentatiecentrum is en waar in de jaren 1880 Margaretha Zelle, beter bekend als Mata Hari, heeft gewoond. Voorzover bekend heeft Eelkje Poppes na haar &lt;i&gt;Eerstelingen&lt;/i&gt; nooit meer iets gepubliceerd. Wel schijnt zij nog enkele kindergedichtjes geschreven te hebben.&lt;/p&gt;Eelkje Poppes overleed op 20 september 1828, 37 jaar oud. De gedenksteen die haar echtgenoot liet aanbrengen in de muur van de kerk in Huizum vermeldt niet alleen haar dood maar ook die van &#8216;vijf onzer kinderen&#8217;. En in een vierregelig vers gedenkt hij het &#8216;aards geluk&#8217; dat ze &#8216;meer dan dertien jaar&#8217; deelden.&lt;br/&gt;&lt;br/&gt;&lt;p&gt;&lt;b&gt;Naslagwerken&lt;/b&gt;&lt;/p&gt;&lt;p&gt;Van der Aa; NBAC.&lt;/p&gt;&lt;p&gt;&lt;b&gt;&lt;br/&gt;Archivalia&lt;/b&gt;&lt;/p&gt;&lt;ul&gt;&lt;li&gt;Koninklijke Bibliotheek, Den Haag: brieven aan Poppes van Robid&#233; van der Aa uit 1815 [sign. 129 E 29].&lt;/li&gt;&lt;li&gt;Universiteitsbibliotheek Amsterdam (UvA), Handschriften: enkele familiedocumenten [Hss. Ce2e, Ce2f].&lt;/li&gt;&lt;/ul&gt;&lt;p&gt;&lt;b&gt;Publicatie&lt;/b&gt;&lt;br/&gt;&lt;i&gt;&lt;br/&gt;Eerstelingen aan mijn vaderland&lt;/i&gt; (Sneek z.j. [1814]) [Knuttel Pflt. 23760].&lt;/p&gt;&lt;b&gt;&lt;br/&gt;Literatuur&lt;/b&gt;&lt;br/&gt;&lt;br/&gt;Sytse ten Hoeve, \'By it portret fan Eelkje Poppes\', &lt;i&gt;De Moanne&lt;/i&gt; 6 (2007) 6, 18-21.&lt;br/&gt;&lt;br/&gt;&lt;b&gt;Illustratie&lt;/b&gt;&lt;br/&gt;&lt;br/&gt;Olieverfportret op paneel, anonieme kunstenaar, ca. 1800 (Particuliere collectie).&lt;br/&gt;&lt;br/&gt;&lt;p&gt;Auteur: Anna de Haas&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</text>\n  </biography>\n</biodes>\n','file:///home/jelle/projects_active/bioport/site/parts/Products/BioPortRepository/tests/data/knaw/003.xml','2010-06-11 08:42:37',NULL),('knaw/004','knaw','<biodes version=\"1.0\">\n  <fileDesc>\n    <title/>\n    <ref target=\"http://www.digitallibrary.nl/levensberichten/authors_detail.cfm?RecordId=1727\"/>\n    <publisher>\n      <name>KNAW - Levensberichten en Herdenkingen</name>\n      <ref target=\"http://www.digitallibrary.nl/levensberichten/works.cfm\"/>\n    </publisher>\n  </fileDesc>\n  <person>\n    <idno type=\"id\">004</idno>\n    <persName>\n        <name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma 4</name>\n	    <name type=\"voornaam\">Franciscus Johannes</name> <name type=\"geslachtsnaam\">St&amp;aacute;amkart</name></persName>\n    <sex value=\"1\"/>\n    <event type=\"birth\" when=\"1805-01-25\">\n      <place>Amsterdam</place>\n    </event>\n    <event type=\"death\" when=\"1882-01-15\">\n      <place>Amsterdam</place>\n    </event>\n    <state type=\"occupation\">Wis- en natuurkunde</state>\n    <state type=\"occupation\">Zeevaartkunde</state>\n  <idno type=\"bioport\">27943051</idno></person>\n  <biography/>\n</biodes>\n','file:///home/jelle/projects_active/bioport/site/parts/Products/BioPortRepository/tests/data/knaw/004.xml','2010-06-11 08:42:37',NULL),('knaw/005','knaw','<biodes version=\"1.0\">\n  <fileDesc>\n    <title/>\n    <ref target=\"http://www.digitallibrary.nl/levensberichten/authors_detail.cfm?RecordId=4610\"/>\n    <publisher>\n      <name>KNAW - Levensberichten en Herdenkingen</name>\n      <ref target=\"http://www.digitallibrary.nl/levensberichten/works.cfm\"/>\n    </publisher>\n  </fileDesc>\n  <person>\n    <idno type=\"id\">005</idno>\n    <persName>Arien A</persName>\n    <sex value=\"1\"/>\n    <event type=\"birth\" when=\"1788-01-01\">\n      <place>Ameide</place>\n    </event>\n    <event type=\"death\" when=\"1847-03-20\"/>\n    <state type=\"occupation\">Wiskunde</state>\n    <state type=\"occupation\">Zeevaartkunde</state>\n  <idno type=\"bioport\">32802206</idno></person>\n  <biography>\n    <text>&lt;body lang=\"EN-US\" style=\"tab-interval:36.0pt;text-justify-trim:punctuation\"&gt;\n&lt;div class=\"Section1\"&gt;\n&lt;p align=\"center\" style=\"margin-right:5.3pt;text-align:center;&amp;#13;&amp;#10;background:white\" class=\"MsoNormal\"&gt;&lt;!--[if gte vml 1]&gt;&lt;v:line id=\"_x0000_s1026\" style=\'position:absolute;&#13;\n left:0;text-align:left;z-index:1;mso-position-horizontal-relative:margin;&#13;\n mso-position-vertical-relative:text\' from=\"-6.5pt,292.55pt\" to=\"-6.5pt,523.65pt\"&#13;\n o:allowincell=\"f\" strokeweight=\"2.15pt\"&gt;&#13;\n &lt;w:wrap anchorx=\"margin\" /&gt;&#13;\n&lt;/v:line&gt;&lt;![endif]--&gt;&lt;span style=\"mso-ignore:vglayout;position:&amp;#13;&amp;#10;absolute;z-index:1;left:0px;margin-left:-11px;margin-top:388px;width:4px;&amp;#13;&amp;#10;height:312px\"&gt;&lt;img width=\"4\" src=\"http://www.digitallibrary.nl:80/files/pub/Jaarboek_1866/xhtml/00001_Jaarboek_1866_P_00001_files/image001.gif\" v:shapes=\"_x0000_s1026\" height=\"312\"/&gt;&lt;/span&gt;&lt;b&gt;&lt;span lang=\"NL\" style=\"font-size:13.0pt;letter-spacing:-.4pt;mso-ansi-language:NL\"&gt;TER&amp;#13;\nGEDACHTENIS&lt;/span&gt;&lt;/b&gt;&lt;/p&gt;\n&lt;p align=\"center\" style=\"margin-top:14.15pt;margin-right:6.95pt;&amp;#13;&amp;#10;margin-bottom:0cm;margin-left:0cm;margin-bottom:.0001pt;text-align:center;&amp;#13;&amp;#10;background:white\" class=\"MsoNormal\"&gt;&lt;b&gt;&lt;span lang=\"NL\" style=\"font-size:6.0pt;letter-spacing:-.1pt;&amp;#13;&amp;#10;mso-ansi-language:NL\"&gt;VAN&lt;/span&gt;&lt;/b&gt;&lt;/p&gt;\n&lt;p style=\"margin-top:13.7pt;margin-right:0cm;margin-bottom:&amp;#13;&amp;#10;0cm;margin-left:3.35pt;margin-bottom:.0001pt;background:white\" class=\"MsoNormal\"&gt;&lt;b&gt;&lt;span lang=\"NL\" style=\"font-size:16.0pt;mso-ansi-language:NL\"&gt;D&lt;sup&gt;R&lt;/sup&gt;. R. C.&amp;#13;\nBAKHUIZEN VAN DEN BRINK.&lt;/span&gt;&lt;/b&gt;&lt;/p&gt;\n&lt;p align=\"center\" style=\"margin-top:11.5pt;margin-right:6.5pt;&amp;#13;&amp;#10;margin-bottom:0cm;margin-left:0cm;margin-bottom:.0001pt;text-align:center;&amp;#13;&amp;#10;background:white\" class=\"MsoNormal\"&gt;&lt;b&gt;&lt;span lang=\"NL\" style=\"font-size:6.0pt;letter-spacing:-.25pt;&amp;#13;&amp;#10;mso-ansi-language:NL\"&gt;DOOR&lt;/span&gt;&lt;/b&gt;&lt;/p&gt;\n&lt;p style=\"margin-top:14.15pt;margin-right:0cm;margin-bottom:&amp;#13;&amp;#10;0cm;margin-left:66.7pt;margin-bottom:.0001pt;background:white\" class=\"MsoNormal\"&gt;&lt;b&gt;&lt;span style=\"font-size:8.0pt\"&gt;I.. &lt;/span&gt;&lt;/b&gt;&lt;b&gt;&lt;span lang=\"NL\" style=\"font-size:8.0pt;&amp;#13;&amp;#10;mso-ansi-language:NL\"&gt;Pb. C. VAN DEN BF.ROH *).&lt;/span&gt;&lt;/b&gt;&lt;/p&gt;\n&lt;p style=\"margin-top:57.6pt;margin-right:2.15pt;margin-bottom:&amp;#13;&amp;#10;0cm;margin-left:0cm;margin-bottom:.0001pt;text-align:justify;text-indent:9.6pt;&amp;#13;&amp;#10;line-height:17pt;13.2pt;mso-line-height:17pt;-rule:exactly;background:white\" class=\"MsoNormal\"&gt;&lt;span lang=\"NL\" style=\"mso-ansi-language:NL\"&gt;Een uitstekend lid is aan dezen kring&amp;#13;\nontvallen, Dr. &lt;span style=\"text-transform:uppercase\"&gt;Rei&amp;#173;nier Coenelis&amp;#13;\nBakhuizen van den Betnk. &lt;/span&gt;Hij is weggemaaid in de volle kracht des&amp;#13;\nlevens, in de volle frischheid van geest, die hem kenmerkte, maar zijne&amp;#13;\nletterkundige en wetenschappe&amp;#173;lijke verdiensten zullen in herinnering blijven,&amp;#13;\nomdat hij de kwijnende letterkunde heeft opgefrischt en de wetenschap voor&amp;#173;uit&amp;#13;\ndoen gaan.&lt;/span&gt;&lt;/p&gt;\n&lt;p style=\"margin-top:0cm;margin-right:1.7pt;margin-bottom:0cm;&amp;#13;&amp;#10;margin-left:.95pt;margin-bottom:.0001pt;text-align:justify;text-indent:8.4pt;&amp;#13;&amp;#10;line-height:17pt;13.2pt;mso-line-height:17pt;-rule:exactly;background:white\" class=\"MsoNormal\"&gt;&lt;span lang=\"NL\" style=\"mso-ansi-language:NL\"&gt;Toen wij na de zomervacantie het eerst&amp;#13;\nweder hier vergader&amp;#173;den, sprak de tijdelijke voorzitter een enkel woord ter&amp;#13;\neere van den ontslapene en herinnerde daarbij te regt, hoe hij een der&amp;#13;\nwerkzaamste leden der akademie geweest was, die, hetzij hij aan de discussie&amp;#13;\nover eenig voorgedragen onderwerp deel nam, hetzij hij zijn oordeel uitbragt&amp;#13;\nover vraagstukken in zijne han&amp;#173;den gesteld, altijd de aandacht zijner medeleden&amp;#13;\nbezig hield, want wat hij sprak was belangrijk van inhoud en puntig van stijl.&amp;#13;\nMaar nooit heeft hij, mijns inziens, zoo belangrijk, zoo uitstekend gesproken,&amp;#13;\nals toen hij zijnen geliefden leermeester &lt;span style=\"text-transform:uppercase\"&gt;Bake&amp;#13;\n&lt;/span&gt;de laatste hulde toebragt. Gij herinnert het u, MHH., hoe hij allen aan&amp;#13;\nzijne lippen boeide en dat, hoe uitvoerig dat&lt;/span&gt;&lt;/p&gt;\n&lt;p style=\"margin-top:18.0pt;margin-right:0cm;margin-bottom:&amp;#13;&amp;#10;0cm;margin-left:2.4pt;margin-bottom:.0001pt;text-indent:5.5pt;line-height:17pt;9.85pt;&amp;#13;&amp;#10;mso-line-height:17pt;-rule:exactly;background:white\" class=\"MsoNormal\"&gt;&lt;b&gt;&lt;span lang=\"NL\" style=\"font-size:8.0pt;mso-ansi-language:NL\"&gt;*) Gelezen in de vergadering der&amp;#13;\nKoninkl. Akad.&lt;span style=\"mso-spacerun:yes\"&gt;&amp;#160; &lt;/span&gt;van Wetenschappen, den&amp;#13;\n18den November 1865.&lt;/span&gt;&lt;/b&gt;&lt;/p&gt;\n&lt;p style=\"margin-top:2.9pt;margin-right:0cm;margin-bottom:0cm;&amp;#13;&amp;#10;margin-left:11.3pt;margin-bottom:.0001pt;tab-stops:235.45pt;background:white\" class=\"MsoNormal\"&gt;&lt;b&gt;&lt;span lang=\"NL\" style=\"font-size:8.0pt;text-transform:uppercase;letter-spacing:-.1pt;&amp;#13;&amp;#10;mso-ansi-language:NL\"&gt;Jaarbokk &lt;/span&gt;&lt;/b&gt;&lt;b&gt;&lt;span lang=\"NL\" style=\"font-size:&amp;#13;&amp;#10;8.0pt;letter-spacing:-.1pt;mso-ansi-language:NL\"&gt;1866.&lt;/span&gt;&lt;/b&gt;&lt;b&gt;&lt;span lang=\"NL\" style=\"font-size:8.0pt;font-family:Arial;mso-hansi-font-family:&amp;quot;Times New Roman&amp;quot;;&amp;#13;&amp;#10;mso-ansi-language:NL\"&gt;&lt;span style=\"mso-tab-count:1\"&gt;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160;&amp;#160; &lt;/span&gt;&lt;/span&gt;&lt;/b&gt;&lt;b&gt;&lt;span lang=\"NL\" style=\"font-size:8.0pt;mso-ansi-language:NL\"&gt;1&lt;/span&gt;&lt;/b&gt;&lt;/p&gt;\n&lt;/div&gt;\n&lt;/body&gt;\n&lt;body lang=\"EN-US\" style=\"tab-interval:36.0pt;text-justify-trim:punctuation\"&gt;\n&lt;div class=\"Section1\"&gt;\n&lt;p align=\"center\" style=\"margin-left:8.65pt;text-align:center;&amp;#13;&amp;#10;background:white\" class=\"MsoNormal\"&gt;&lt;!--[if gte vml 1]&gt;&lt;v:line id=\"_x0000_s1026\" style=\'position:absolute;&#13;\n left:0;text-align:left;z-index:1;mso-position-horizontal-relative:margin;&#13;\n mso-position-vertical-relative:text\' from=\"278.15pt,315.35pt\" to=\"278.15pt,544.3pt\"&#13;\n o:allowincell=\"f\" strokeweight=\"1.2pt\"&gt;&#13;\n &lt;w:wrap anchorx=\"margin\" /&gt;&#13;\n&lt;/v:line&gt;&lt;![endif]--&gt;&lt;span style=\"mso-ignore:vglayout;position:&amp;#13;&amp;#10;absolute;z-index:1;left:0px;margin-left:370px;margin-top:419px;width:2px;&amp;#13;&amp;#10;height:308px\"&gt;&lt;img width=\"2\" src=\"http://www.digitallibrary.nl:80/files/pub/Jaarboek_1866/xhtml/00002_Jaarboek_1866_P_00002_files/image001.gif\" v:shapes=\"_x0000_s1026\" height=\"308\"/&gt;&lt;/span&gt;&lt;b&gt;&lt;span lang=\"NL\" style=\"font-size:9.0pt;font-family:Arial;mso-ansi-language:NL\"&gt;( 2 )&lt;/span&gt;&lt;/b&gt;&lt;/p&gt;\n&lt;p style=\"margin-top:8.65pt;margin-right:0cm;margin-bottom:&amp;#13;&amp;#10;0cm;margin-left:3.85pt;margin-bottom:.0001pt;text-align:justify;line-height:17pt;&amp;#13;&amp;#10;13.2pt;mso-line-height:17pt;-rule:exactly;background:white\" class=\"MsoNormal\"&gt;&lt;span lang=\"NL\" style=\"mso-ansi-language:NL\"&gt;stuk ook was, niemand het te lang vond. Dat was&amp;#13;\nzijn zwa&amp;#173;nenzang. Slechts een jaar daarna wordt ook hij hier herdacht en het&amp;#13;\ntafereel van zyn leven e&amp;#187; werken volgt op dat van zij&amp;#173;nen leermeester.&lt;/span&gt;&lt;/p&gt;\n&lt;p style=\"margin-top:0cm;margin-right:.25pt;margin-bottom:0cm;&amp;#13;&amp;#10;margin-left:1.45pt;margin-bottom:.0001pt;text-align:justify;text-indent:11.75pt;&amp;#13;&amp;#10;line-height:17pt;13.2pt;mso-line-height:17pt;-rule:exactly;background:white\" class=\"MsoNormal\"&gt;&lt;span lang=\"NL\" style=\"mso-ansi-language:NL\"&gt;Het werd mij opgedragen dat tafereel te&amp;#13;\nschetsen. Ik heb lang geaarzeld eer ik die moeijelijke taak aanvaardde, waut&amp;#13;\nmijne betrekking tot den overledene dagteekent slechts van zijne plaatsing aan&amp;#13;\nhet rijksarchief of weinig eerder. Van zijn vroe&amp;#173;ger veelbewogen leven, van&amp;#13;\nzijn werken en schrijven was mij slechts een gedeelte, en dat nog onvolledig,&amp;#13;\nbekend en eene poging om inlichtingen te verkrijgen, bij een zijner vroegere&amp;#13;\nmedearbeiders op het veld der letterkunde aangewend, werd afgewezen. Maar toen&amp;#13;\nieder zijner vrienden zich van die. taak verschoonde, meende ik verpligt te&amp;#13;\nzijn ook met gebrekkige hulpmiddelen op te treden, omdat ik vooral wenschte,&amp;#13;\ndat zijne &lt;span style=\"letter-spacing:-.05pt\"&gt;groote verdiensten omtrent het&amp;#13;\narchiefwezen algemeen bekend en &lt;/span&gt;erkend worden en niemand zoo naauwkeurig&amp;#13;\ndaarvan berigt kon geven als zijn veeljarige vriend en medearbeider, die meer&amp;#13;\ndan twaalf jaren dagelijks met hem daaraan zijne krachten gewijd heeft Die&amp;#13;\nbeweegreden moge het gebrekkige van den vorm en het onvolledige van den inhoud&amp;#13;\nverschoonen.&lt;/span&gt;&lt;/p&gt;\n&lt;p style=\"margin-top:0cm;margin-right:3.1pt;margin-bottom:0cm;&amp;#13;&amp;#10;margin-left:.5pt;margin-bottom:.0001pt;text-align:justify;text-indent:11.05pt;&amp;#13;&amp;#10;line-height:17pt;13.2pt;mso-line-height:17pt;-rule:exactly;background:white\" class=\"MsoNormal\"&gt;&lt;span lang=\"NL\" style=\"mso-ansi-language:NL\"&gt;Er zijn velen, wier biograaph zorgvuldig&amp;#13;\nalle gebreken be-mantelen en daarentegen elke goede zijde helder moet doen&amp;#13;\nuitkomen, wil hij bij den lezer of hoorder nog eenige belang&amp;#173;stelling voor&amp;#13;\nzijnen held opwekken. Dat is het geval met de meesten, voor wie jaarlijks in de&amp;#13;\ngenootschappen de doodklok geluid wordt; maar er zijn ook enkelen, wier&amp;#13;\ngebreken men on&amp;#173;bevreesd erkennen mag, omdat er meer voortreffelijk&amp;#187; tegenover&amp;#13;\nstaat, en zij ook met die menschelijke zwakheden een belangrijk leven geleefd&amp;#13;\nhebben.&lt;span style=\"mso-spacerun:yes\"&gt;&amp;#160;&amp;#160;&amp;#160; &lt;/span&gt;Tot die weinigen behoorde &lt;span style=\"text-transform:uppercase\"&gt;Bakhuizen.&lt;/span&gt;&lt;/span&gt;&lt;/p&gt;\n&lt;p style=\"margin-top:.25pt;margin-right:4.1pt;margin-bottom:&amp;#13;&amp;#10;0cm;margin-left:0cm;margin-bottom:.0001pt;text-align:justify;text-indent:11.75pt;&amp;#13;&amp;#10;line-height:17pt;13.2pt;mso-line-height:17pt;-rule:exactly;background:white\" class=\"MsoNormal\"&gt;&lt;span lang=\"NL\" style=\"mso-ansi-language:NL\"&gt;Hij was een volbloed Amsterdammer, zoowel&amp;#13;\nvan afkomst als van genegenheid. Geboren den 28&lt;sup&gt;8ten&lt;/sup&gt; Februari] 1810,&amp;#13;\ngenoot hij aan het gymnasium dezer stad zijne eerste opleiding tot de&amp;#13;\nwetenschap, onder den toenmaligen rector &lt;span style=\"text-transform:uppercase\"&gt;Zilubskn.&amp;#13;\n&lt;/span&gt;Daarop hoorde hij de lessen aan het athenaeum, bestemd, hetzij dan door&amp;#13;\nzijne ouders of naar eigene keus, voor de theologie. Maar om tot dat heiligdom&amp;#13;\nin te gaan, moest hij eerst door den aan-&lt;/span&gt;&lt;/p&gt;\n&lt;/div&gt;\n&lt;/body&gt;\n&lt;body lang=\"EN-US\" style=\"tab-interval:36.0pt;text-justify-trim:punctuation\"&gt;\n&lt;div class=\"Section1\"&gt;\n&lt;p align=\"center\" style=\"margin-right:5.05pt;text-align:center;&amp;#13;&amp;#10;background:white\" class=\"MsoNormal\"&gt;&lt;!--[if gte vml 1]&gt;&lt;v:line id=\"_x0000_s1026\" style=\'position:absolute;&#13;\n left:0;text-align:left;z-index:1;mso-position-horizontal-relative:margin;&#13;\n mso-position-vertical-relative:text\' from=\"-7.2pt,244.1pt\" to=\"-7.2pt,455.05pt\"&#13;\n o:allowincell=\"f\" strokeweight=\".5pt\"&gt;&#13;\n &lt;w:wrap anchorx=\"margin\" /&gt;&#13;\n&lt;/v:line&gt;&lt;![endif]--&gt;&lt;span style=\"mso-ignore:vglayout;position:&amp;#13;&amp;#10;absolute;z-index:1;left:0px;margin-left:-11px;margin-top:324px;width:2px;&amp;#13;&amp;#10;height:284px\"&gt;&lt;img width=\"2\" src=\"http://www.digitallibrary.nl:80/files/pub/Jaarboek_1866/xhtml/00003_Jaarboek_1866_P_00003_files/image001.gif\" v:shapes=\"_x0000_s1026\" height=\"284\"/&gt;&lt;/span&gt;&lt;b&gt;&lt;span lang=\"NL\" style=\"font-family:Arial;mso-ansi-language:NL\"&gt;(3)&lt;/span&gt;&lt;/b&gt;&lt;/p&gt;\n&lt;p style=\"margin-top:8.65pt;margin-right:1.9pt;margin-bottom:&amp;#13;&amp;#10;0cm;margin-left:0cm;margin-bottom:.0001pt;text-align:justify;line-height:17pt;13.2pt;&amp;#13;&amp;#10;mso-line-height:17pt;-rule:exactly;background:white\" class=\"MsoNormal\"&gt;&lt;span lang=\"NL\" style=\"mso-ansi-language:&amp;#13;&amp;#10;NL\"&gt;lokkenden tuin der philologie en daar boeide hem vooral de smaakvolle&amp;#13;\nvoordragt van den hoogleeraar &lt;span style=\"text-transform:uppercase\"&gt;van&amp;#13;\nLennkp. &lt;/span&gt;Nog in lateren tijd gewaagde hij dikwijls met welgevallen van&amp;#13;\nhet&amp;#173;geen hij van dezen gehoord had en hij heeft dan ook bij diens overlijden&amp;#13;\nzijn aandenken dankbaar gevierd in een artikel, op&amp;#173;genomen in het tijdschrift &lt;i&gt;de&amp;#13;\nletterbode. &lt;/i&gt;Toch verwaarloosde hij daarom de studie der godgeleerdheid niet&amp;#13;\nen hij heeft mij meermalen verklaard, dat hij inzonderheid de &lt;i&gt;historia&amp;#13;\ndogmatum &lt;/i&gt;met belangstelling beoefend had, waarschijnlijk geleid door zijne&amp;#13;\ntoenmalige philosophische studi&amp;#235;n.&lt;/span&gt;&lt;/p&gt;\n&lt;p style=\"margin-top:.5pt;margin-right:.25pt;margin-bottom:&amp;#13;&amp;#10;0cm;margin-left:1.45pt;margin-bottom:.0001pt;text-align:justify;text-indent:&amp;#13;&amp;#10;9.85pt;line-height:17pt;13.2pt;mso-line-height:17pt;-rule:exactly;background:white\" class=\"MsoNormal\"&gt;&lt;span lang=\"NL\" style=\"mso-ansi-language:NL\"&gt;Na te Amsterdam eene poos gestudeerd te&amp;#13;\nhebben, vertrok hij naar Leiden om daar zijne studi&amp;#235;n te voltooijen. Hier slqeg&amp;#13;\nhij de wieken uit: aan den eenen kant genoot hij volop de vrij&amp;#173;heid en de&amp;#13;\nvreugd van het studentenleven, zelfs wel eens meer dan nuttig was, maar aan den&amp;#13;\nanderen kant zwelgde hij even&amp;#173;zeer in de genietingen der wetenschap. Wat hij&amp;#13;\nwas, was hij geheel en rondborstig. Dartel en overmoedig, maar goedhartig en&amp;#13;\noorspronkelijk, was hij onder vrienden de vrolijkste, de wild&amp;#173;ste, aan zijne&amp;#13;\nstudeertafel de onvermoeidste. Een zijner tijdgenoo-ten aan de akademie&amp;#13;\nverhaalde mij, dat meer dan eens, na een gloeijend studentenfeest, waar hij de&amp;#13;\nuitgelatenste, de meest ru&amp;#173;moerige van allen geweest was, wanneer men eindelijk&amp;#13;\nin het holle van den nacht uiteen ging en anderen afgemat naar huis waggelden&amp;#13;\nen op hun bed neerzonken, hij dan zijne lamp aan&amp;#173;stak om zich in Pindarus te&amp;#13;\nverdienen.&lt;/span&gt;&lt;/p&gt;\n&lt;p style=\"margin-top:.5pt;margin-right:0cm;margin-bottom:0cm;&amp;#13;&amp;#10;margin-left:3.85pt;margin-bottom:.0001pt;text-align:justify;text-indent:8.9pt;&amp;#13;&amp;#10;line-height:17pt;13.2pt;mso-line-height:17pt;-rule:exactly;background:white\" class=\"MsoNormal\"&gt;&lt;span lang=\"NL\" style=\"mso-ansi-language:NL\"&gt;Toch had hij eindelijk in dat&amp;#13;\nstudentikoose leven geheel knn-nen ondergaan, had hij niet te Leiden twee&amp;#13;\nmannen gevonden, die als goede genii hem ter zijde stonden en die hem voor de&amp;#13;\nwetenschap behielden, &lt;span style=\"text-transform:uppercase\"&gt;Bake &lt;/span&gt;en &lt;span style=\"text-transform:uppercase\"&gt;Geel. &lt;/span&gt;Wat hij aan den eerste te danken&amp;#13;\nhad heeft hij zelf het vorige jaar in warme taal uit&amp;#173;gesproken, wat de ander&amp;#13;\nvoor hem was blijkt uit zijne brieven &lt;span style=\"letter-spacing:-.05pt\"&gt;en&amp;#13;\nerkent hij zelf in zijne &lt;i&gt;Epistola critica ad faeobum Geelium, &lt;/i&gt;&lt;/span&gt;opgenomen&amp;#13;\nia het vijfde deel der &lt;i&gt;Sym&amp;#232;olae litemriae. &lt;/i&gt;#Norunt omnes (zegt bij&amp;#13;\ndaar), qui literarum disciplinae haud &lt;i&gt;fiavavat-%&amp;lt;ag &lt;/i&gt;incumbant, quauto&amp;#13;\neos amplecti amore, quamque eos in sinu veluti gestare consueveris: ego vero in&amp;#13;\npaucis haud magis te artis magistrum quam consiliorum&lt;span style=\"mso-spacerun:yes\"&gt;&amp;#160; &lt;/span&gt;totiusque vitae&lt;span style=\"mso-spacerun:yes\"&gt;&amp;#160; &lt;/span&gt;praecep-&lt;/span&gt;&lt;/p&gt;\n&lt;p style=\"margin-left:232.3pt;line-height:17pt;13.2pt;mso-line-height:17pt;-rule:&amp;#13;&amp;#10;exactly;background:white\" class=\"MsoNormal\"&gt;&lt;span lang=\"NL\" style=\"mso-ansi-language:NL\"&gt;1*&lt;/span&gt;&lt;/p&gt;\n&lt;/div&gt;\n&lt;/body&gt;\n    </text>  \n  </biography>\n</biodes>\n','file:///home/jelle/projects_active/bioport/site/parts/Products/BioPortRepository/tests/data/knaw/005.xml','2010-06-11 08:42:37',NULL),('knaw2/006','knaw2','<biodes version=\"1.0\">\n  <fileDesc>\n    <title/>\n    <author>Tex, C.A. den</author>\n    <ref target=\"http://www.digitallibrary.nl/levensberichten/authors_detail.cfm?RecordId=4484\"/>\n    <publisher>\n      <name>KNAW - Levensberichten en Herdenkingen</name>\n      <ref target=\"http://www.digitallibrary.nl/levensberichten/works.cfm\"/>\n    </publisher>\n  </fileDesc>\n  <person>\n    <idno type=\"id\">006</idno>\n    <persName><name type=\"voornaam\">Hilbrand MolloyX</name> <name type=\"geslachtsnaam\">Boschma</name></persName>\n    <persName><name type=\"voornaam\">Cornelis</name> <name type=\"geslachtsnaam\">Ekama</name></persName>\n    <sex value=\"1\"/>\n    <event type=\"birth\" when=\"1773-03-31\">\n      <place>Paesens, Frankrijk</place>\n    </event>\n    <event type=\"death\" when=\"1826-02-24\">\n      <place>Leiden</place>\n    </event>\n    <state type=\"occupation\">Natuurkunde</state>\n    <state type=\"occupation\">Zeevaartkunde</state>\n  <idno type=\"bioport\">31132281</idno></person>\n  <biography/>\n</biodes>\n','file:///home/jelle/projects_active/bioport/site/parts/Products/BioPortRepository/tests/data/knaw2/006.xml','2010-06-11 08:42:37',NULL),('knaw2/007','knaw2','<biodes version=\"1.0\">\n  <fileDesc>\n    <title/>\n    <ref target=\"http://www.digitallibrary.nl/levensberichten/authors_detail.cfm?RecordId=4438\"/>\n    <publisher>\n      <name>KNAW - Levensberichten en Herdenkingen</name>\n      <ref target=\"http://www.digitallibrary.nl/levensberichten/works.cfm\"/>\n    </publisher>\n  </fileDesc>\n  <person>\n    <idno type=\"id\">007</idno>\n    <persName><name type=\"voornaam\">Pierre Emmanuel</name> <name type=\"geslachtsnaam\">Stamkart</name></persName>\n    <persName><name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma</name></persName>\n    <sex value=\"1\"/>\n    <event type=\"birth\" when=\"1750-01-01\">\n      <place>Gent, Belgi&#235;</place>\n    </event>\n    <event type=\"death\" when=\"1819-11-01\">\n      <place>Gent, Belgi&#235;</place>\n    </event>\n    <state type=\"occupation\">Componist</state>\n    <state type=\"occupation\">Zanger</state>\n    <state type=\"occupation\">Dirigent</state>\n  <idno type=\"bioport\">15590559</idno></person>\n  <biography/>\n</biodes>\n','file:///home/jelle/projects_active/bioport/site/parts/Products/BioPortRepository/tests/data/knaw2/007.xml','2010-06-11 08:42:37',NULL),('knaw2/008','knaw2','<biodes version=\"1.0\">\n  <fileDesc>\n    <title/>\n    <author>Korteweg, D.J.</author>\n    <ref target=\"http://www.digitallibrary.nl/levensberichten/authors_detail.cfm?RecordId=1262\"/>\n    <publisher>\n      <name>KNAW - Levensberichten en Herdenkingen</name>\n      <ref target=\"http://www.digitallibrary.nl/levensberichten/works.cfm\"/>\n    </publisher>\n  </fileDesc>\n  <person>\n    <idno type=\"id\">008</idno>\n    <persName><name type=\"voornaam\">Nicolaas Theodoor</name> <name type=\"geslachtsnaam\">Micha&#235;lis</name></persName>\n    <persName><name type=\"voornaam\">Hendrik</name> <name type=\"geslachtsnaam\">Kraemer</name></persName>\n    <persName><name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma twee</name></persName>\n    <sex value=\"1\"/>\n    <event type=\"birth\" when=\"1824-12-03\">\n      <place>Brussel, Belgi&#235;</place>\n    </event>\n    <event type=\"death\" when=\"1904-05-15\">\n      <place>\'s Gravenhage</place>\n    </event>\n    <state type=\"occupation\">Waterstaatkunde</state>\n    <state type=\"occupation\">Wiskunde</state>\n    <state type=\"occupation\">Bruggenbouw</state>\n  <idno type=\"bioport\">38318174</idno></person>\n  <biography/>\n</biodes>\n','file:///home/jelle/projects_active/bioport/site/parts/Products/BioPortRepository/tests/data/knaw2/008.xml','2010-06-11 08:42:37',NULL),('knaw2/00a','knaw2','<biodes version=\"1.0\">\n  <fileDesc>\n    <title/>\n    <author>Hooykaas, R.</author>\n    <ref target=\"http://www.digitallibrary.nl/levensberichten/authors_detail.cfm?RecordId=478\"/>\n    <publisher>\n      <name>KNAW - Levensberichten en Herdenkingen</name>\n      <ref target=\"http://www.digitallibrary.nl/levensberichten/works.cfm\"/>\n    </publisher>\n  </fileDesc>\n  <person>\n    <idno type=\"id\">00a</idno>\n    <persName><name type=\"voornaam\">Eduard Jan</name> <name type=\"geslachtsnaam\">Dijksterhuis</name></persName>\n    <persName><name type=\"voornaam\">C.</name> <name type=\"intrapositie\">van</name> <name type=\"geslachtsnaam\">Heynsbergen</name></persName>\n    <persName><name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma twee</name></persName>\n    <sex value=\"1\"/>\n    <event type=\"birth\" when=\"1892-10-28\">\n      <place>Tilburg</place>\n    </event>\n    <event type=\"death\" when=\"1965-05-18\">\n      <place>De Bilt</place>\n    </event>\n    <state type=\"occupation\">Geschiedenis der exacte wetenschappen</state>\n    <state type=\"occupation\">Wiskunde</state>\n  <idno type=\"bioport\">28104076</idno></person>\n  <biography/>\n</biodes>\n','file:///home/jelle/projects_active/bioport/site/parts/Products/BioPortRepository/tests/data/knaw2/009.xml','2010-06-11 08:42:37',NULL),('knaw2/00A','knaw2','<biodes version=\"1.0\">\n  <fileDesc>\n    <title/>\n    <ref target=\"http://www.digitallibrary.nl/levensberichten/authors_detail.cfm?RecordId=393\"/>\n    <publisher>\n      <name>KNAW - Levensberichten en Herdenkingen</name>\n      <ref target=\"http://www.digitallibrary.nl/levensberichten/works.cfm\"/>\n    </publisher>\n  </fileDesc>\n  <person>\n    <idno type=\"id\">00A</idno>\n    <persName><name type=\"voornaam\">George Howard</name> <name type=\"geslachtsnaam\">Darwin</name></persName>\n    <persName><name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma</name></persName>\n    <sex value=\"1\"/>\n    <event type=\"birth\" when=\"1845-07-09\">\n      <place>Down, Groot Brittani&#235;</place>\n    </event>\n    <event type=\"death\" when=\"1912-12-07\">\n      <place>Newham, Groot Brittani&#235;</place>\n    </event>\n    <state type=\"occupation\">Sterrenkunde</state>\n    <state type=\"occupation\">Wiskunde</state>\n  <idno type=\"bioport\">75994708</idno></person>\n  <biography/>\n</biodes>\n','file:///home/jelle/projects_active/bioport/site/parts/Products/BioPortRepository/tests/data/knaw2/010.xml','2010-06-11 08:42:38',NULL);
/*!40000 ALTER TABLE `biography` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bioportid`
--

DROP TABLE IF EXISTS `bioportid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bioportid` (
  `bioport_id` varchar(50) NOT NULL,
  `redirect_to` varchar(50) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`bioport_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bioportid`
--

LOCK TABLES `bioportid` WRITE;
/*!40000 ALTER TABLE `bioportid` DISABLE KEYS */;
INSERT INTO `bioportid` VALUES ('27201748',NULL,'2010-06-11 08:42:37'),('84972544',NULL,'2010-06-11 08:42:37'),('44333513',NULL,'2010-06-11 08:42:37'),('27943051',NULL,'2010-06-11 08:42:37'),('32802206',NULL,'2010-06-11 08:42:37'),('31132281',NULL,'2010-06-11 08:42:37'),('15590559',NULL,'2010-06-11 08:42:37'),('38318174',NULL,'2010-06-11 08:42:37'),('28104076',NULL,'2010-06-11 08:42:37'),('75994708',NULL,'2010-06-11 08:42:38');
/*!40000 ALTER TABLE `bioportid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cache_similarity`
--

DROP TABLE IF EXISTS `cache_similarity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cache_similarity` (
  `naam1_id` int(11) NOT NULL,
  `naam2_id` int(11) NOT NULL,
  `score` float DEFAULT NULL,
  PRIMARY KEY (`naam1_id`,`naam2_id`),
  KEY `ix_cache_similarity_naam2_id` (`naam2_id`),
  KEY `ix_cache_similarity_score` (`score`),
  KEY `ix_cache_similarity_naam1_id` (`naam1_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cache_similarity`
--

LOCK TABLES `cache_similarity` WRITE;
/*!40000 ALTER TABLE `cache_similarity` DISABLE KEYS */;
/*!40000 ALTER TABLE `cache_similarity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cache_similarity_persons`
--

DROP TABLE IF EXISTS `cache_similarity_persons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cache_similarity_persons` (
  `bioport_id1` varchar(50) NOT NULL,
  `bioport_id2` varchar(50) NOT NULL,
  `score` float DEFAULT NULL,
  PRIMARY KEY (`bioport_id1`,`bioport_id2`),
  KEY `ix_cache_similarity_persons_bioport_id2` (`bioport_id2`),
  KEY `ix_cache_similarity_persons_bioport_id1` (`bioport_id1`),
  KEY `ix_cache_similarity_persons_score` (`score`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cache_similarity_persons`
--

LOCK TABLES `cache_similarity_persons` WRITE;
/*!40000 ALTER TABLE `cache_similarity_persons` DISABLE KEYS */;
/*!40000 ALTER TABLE `cache_similarity_persons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_category_name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Adel en vorstenhuizen'),(2,'Bedrijfsleven'),(3,'Beeldende kunsten & vormgeving'),(4,'Kerk en godsdienst'),(5,'Koloniale en overzeese betrekkingen en handel'),(6,'Krijgsmacht en oorlog'),(7,'Letterkunde'),(8,'Maatschappelijke bewegingen'),(9,'Rechtspraak'),(10,'Onderwijs & wetenschappen'),(11,'Politiek en bestuur'),(12,'Radio en TV'),(14,'Sport en vrije tijd'),(15,'Uitvoerende kunsten'),(16,'Zorg'),(17,'Overig');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `changelog`
--

DROP TABLE IF EXISTS `changelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `changelog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `table` varchar(50) DEFAULT NULL,
  `record_id_int` int(11) DEFAULT NULL,
  `record_id_str` varchar(255) DEFAULT NULL,
  `msg` text,
  `user` varchar(50) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_changelog_record_id_int` (`record_id_int`),
  KEY `ix_changelog_table` (`table`),
  KEY `ix_changelog_record_id_str` (`record_id_str`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `changelog`
--

LOCK TABLES `changelog` WRITE;
/*!40000 ALTER TABLE `changelog` DISABLE KEYS */;
INSERT INTO `changelog` VALUES (1,'source',NULL,'knaw','Added source','Uknown User','2010-06-11 08:42:37'),(2,'bioportid',NULL,'27201748','Added bioport_id %s to the registry','Uknown User','2010-06-11 08:42:37'),(3,'biography',NULL,'knaw/001','saved biography with id knaw/001','Uknown User','2010-06-11 08:42:37'),(4,'bioportid',NULL,'84972544','Added bioport_id %s to the registry','Uknown User','2010-06-11 08:42:37'),(5,'biography',NULL,'knaw/002','saved biography with id knaw/002','Uknown User','2010-06-11 08:42:37'),(6,'bioportid',NULL,'44333513','Added bioport_id %s to the registry','Uknown User','2010-06-11 08:42:37'),(7,'biography',NULL,'knaw/003','saved biography with id knaw/003','Uknown User','2010-06-11 08:42:37'),(8,'bioportid',NULL,'27943051','Added bioport_id %s to the registry','Uknown User','2010-06-11 08:42:37'),(9,'biography',NULL,'knaw/004','saved biography with id knaw/004','Uknown User','2010-06-11 08:42:37'),(10,'bioportid',NULL,'32802206','Added bioport_id %s to the registry','Uknown User','2010-06-11 08:42:37'),(11,'biography',NULL,'knaw/005','saved biography with id knaw/005','Uknown User','2010-06-11 08:42:37'),(12,'source',NULL,'knaw2','Added source','Uknown User','2010-06-11 08:42:37'),(13,'bioportid',NULL,'31132281','Added bioport_id %s to the registry','Uknown User','2010-06-11 08:42:37'),(14,'biography',NULL,'knaw2/006','saved biography with id knaw2/006','Uknown User','2010-06-11 08:42:37'),(15,'bioportid',NULL,'15590559','Added bioport_id %s to the registry','Uknown User','2010-06-11 08:42:37'),(16,'biography',NULL,'knaw2/007','saved biography with id knaw2/007','Uknown User','2010-06-11 08:42:37'),(17,'bioportid',NULL,'38318174','Added bioport_id %s to the registry','Uknown User','2010-06-11 08:42:37'),(18,'biography',NULL,'knaw2/008','saved biography with id knaw2/008','Uknown User','2010-06-11 08:42:37'),(19,'bioportid',NULL,'28104076','Added bioport_id %s to the registry','Uknown User','2010-06-11 08:42:37'),(20,'biography',NULL,'knaw2/00a','saved biography with id knaw2/00a','Uknown User','2010-06-11 08:42:38'),(21,'bioportid',NULL,'75994708','Added bioport_id %s to the registry','Uknown User','2010-06-11 08:42:38'),(22,'biography',NULL,'knaw2/00A','saved biography with id knaw2/00A','Uknown User','2010-06-11 08:42:38');
/*!40000 ALTER TABLE `changelog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bioport_id` varchar(50) DEFAULT NULL,
  `text` text,
  `created` datetime DEFAULT NULL,
  `submitter` varchar(20) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_comment_bioport_id` (`bioport_id`),
  KEY `ix_comment_created` (`created`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dbnl_ids`
--

DROP TABLE IF EXISTS `dbnl_ids`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbnl_ids` (
  `bioport_id1` varchar(50) NOT NULL,
  `bioport_id2` varchar(50) NOT NULL,
  `source1` varchar(5) DEFAULT NULL,
  `source2` varchar(5) DEFAULT NULL,
  `dbnl_id` varchar(20) DEFAULT NULL,
  `score` float DEFAULT NULL,
  PRIMARY KEY (`bioport_id1`,`bioport_id2`),
  KEY `ix_dbnl_ids_bioport_id2` (`bioport_id2`),
  KEY `ix_dbnl_ids_bioport_id1` (`bioport_id1`),
  KEY `ix_dbnl_ids_score` (`score`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dbnl_ids`
--

LOCK TABLES `dbnl_ids` WRITE;
/*!40000 ALTER TABLE `dbnl_ids` DISABLE KEYS */;
/*!40000 ALTER TABLE `dbnl_ids` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `defer_identification`
--

DROP TABLE IF EXISTS `defer_identification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `defer_identification` (
  `bioport_id1` varchar(50) NOT NULL,
  `bioport_id2` varchar(50) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`bioport_id1`,`bioport_id2`),
  KEY `bioport_id2` (`bioport_id2`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `defer_identification`
--

LOCK TABLES `defer_identification` WRITE;
/*!40000 ALTER TABLE `defer_identification` DISABLE KEYS */;
/*!40000 ALTER TABLE `defer_identification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `location` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ufi` int(11) DEFAULT NULL,
  `uni` int(11) DEFAULT NULL,
  `long` float DEFAULT NULL,
  `lat` float DEFAULT NULL,
  `adm1` varchar(2) DEFAULT NULL,
  `sort_name` varchar(100) DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_location_sort_name` (`sort_name`),
  KEY `ix_location_adm1` (`adm1`),
  KEY `ix_location_full_name` (`full_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location`
--

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `naam`
--

DROP TABLE IF EXISTS `naam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `naam` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sort_key` varchar(100) DEFAULT NULL,
  `snippet` text,
  `birth` varchar(10) DEFAULT NULL,
  `death` varchar(10) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `src` varchar(255) DEFAULT NULL,
  `xml` text,
  `volledige_naam` varchar(255) DEFAULT NULL,
  `url_description` text,
  `territoriale_titel` varchar(255) DEFAULT NULL,
  `variant_of` int(11) DEFAULT NULL,
  `bioport_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `variant_of` (`variant_of`),
  KEY `ix_naam_bioport_id` (`bioport_id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `naam`
--

LOCK TABLES `naam` WRITE;
/*!40000 ALTER TABLE `naam` DISABLE KEYS */;
INSERT INTO `naam` VALUES (1,'boschma hilbrand',NULL,NULL,NULL,NULL,'knaw','<persName><name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma</name></persName>','Boschma, Hilbrand',NULL,NULL,NULL,'27201748'),(2,'boschma twee hilbrand',NULL,NULL,NULL,NULL,'knaw','<persName><name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma twee</name></persName>','Boschma twee, Hilbrand',NULL,NULL,NULL,'84972544'),(3,'boschma kraemer hilbrand hendrik',NULL,NULL,NULL,NULL,'knaw','<persName>\n        <name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma</name>\n        <name type=\"voornaam\">Hendrik</name> <name type=\"geslachtsnaam\">Kraemer</name>\n    </persName>','Boschma Kraemer, Hilbrand Hendrik',NULL,NULL,NULL,'44333513'),(4,'boschma 4 st&aacute;amkart hilbrand fran',NULL,NULL,NULL,NULL,'knaw','<persName>\n        <name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma 4</name>\n	    <name type=\"voornaam\">Franciscus Johannes</name> <name type=\"geslachtsnaam\">St&amp;aacute;amkart</name></persName>','Boschma 4 St&aacute;amkart, Hilbrand Franciscus Johannes',NULL,NULL,NULL,'27943051'),(5,'a arien',NULL,NULL,NULL,NULL,'knaw','<persName>Arien <name type=\"geslachtsnaam\">A</name></persName>','A, Arien',NULL,NULL,NULL,'32802206'),(6,'boschma hilbrand molloyx',NULL,NULL,NULL,NULL,'knaw2','<persName><name type=\"voornaam\">Hilbrand MolloyX</name> <name type=\"geslachtsnaam\">Boschma</name></persName>','Boschma, Hilbrand Molloyx',NULL,NULL,NULL,'31132281'),(7,'ekama cornelis',NULL,NULL,NULL,NULL,'knaw2','<persName><name type=\"voornaam\">Cornelis</name> <name type=\"geslachtsnaam\">Ekama</name></persName>','Ekama, Cornelis',NULL,NULL,NULL,'31132281'),(8,'stamkart pierre emmanuel',NULL,NULL,NULL,NULL,'knaw2','<persName><name type=\"voornaam\">Pierre Emmanuel</name> <name type=\"geslachtsnaam\">Stamkart</name></persName>','Stamkart, Pierre Emmanuel',NULL,NULL,NULL,'15590559'),(9,'boschma hilbrand',NULL,NULL,NULL,NULL,'knaw2','<persName><name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma</name></persName>','Boschma, Hilbrand',NULL,NULL,NULL,'15590559'),(10,'michaelis nicolaas theodoor',NULL,NULL,NULL,NULL,'knaw2','<persName><name type=\"voornaam\">Nicolaas Theodoor</name> <name type=\"geslachtsnaam\">MichaÃ«lis</name></persName>','MichaÃ«lis, Nicolaas Theodoor',NULL,NULL,NULL,'38318174'),(11,'kraemer hendrik',NULL,NULL,NULL,NULL,'knaw2','<persName><name type=\"voornaam\">Hendrik</name> <name type=\"geslachtsnaam\">Kraemer</name></persName>','Kraemer, Hendrik',NULL,NULL,NULL,'38318174'),(12,'boschma twee hilbrand',NULL,NULL,NULL,NULL,'knaw2','<persName><name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma twee</name></persName>','Boschma twee, Hilbrand',NULL,NULL,NULL,'38318174'),(13,'dijksterhuis eduard jan',NULL,NULL,NULL,NULL,'knaw2','<persName><name type=\"voornaam\">Eduard Jan</name> <name type=\"geslachtsnaam\">Dijksterhuis</name></persName>','Dijksterhuis, Eduard Jan',NULL,NULL,NULL,'28104076'),(14,'heynsbergen c. van',NULL,NULL,NULL,NULL,'knaw2','<persName><name type=\"voornaam\">C.</name> <name type=\"intrapositie\">van</name> <name type=\"geslachtsnaam\">Heynsbergen</name></persName>','Heynsbergen, C. van',NULL,NULL,NULL,'28104076'),(15,'boschma twee hilbrand',NULL,NULL,NULL,NULL,'knaw2','<persName><name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma twee</name></persName>','Boschma twee, Hilbrand',NULL,NULL,NULL,'28104076'),(16,'darwin george howard',NULL,NULL,NULL,NULL,'knaw2','<persName><name type=\"voornaam\">George Howard</name> <name type=\"geslachtsnaam\">Darwin</name></persName>','Darwin, George Howard',NULL,NULL,NULL,'75994708'),(17,'boschma hilbrand',NULL,NULL,NULL,NULL,'knaw2','<persName><name type=\"voornaam\">Hilbrand</name> <name type=\"geslachtsnaam\">Boschma</name></persName>','Boschma, Hilbrand',NULL,NULL,NULL,'75994708');
/*!40000 ALTER TABLE `naam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `occupation`
--

DROP TABLE IF EXISTS `occupation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `occupation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_occupation_name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `occupation`
--

LOCK TABLES `occupation` WRITE;
/*!40000 ALTER TABLE `occupation` DISABLE KEYS */;
/*!40000 ALTER TABLE `occupation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person` (
  `bioport_id` varchar(50) NOT NULL,
  `geboortedatum` varchar(10) DEFAULT NULL,
  `geboortejaar` int(11) DEFAULT NULL,
  `geboorteplaats` varchar(255) DEFAULT NULL,
  `sterfdatum` varchar(10) DEFAULT NULL,
  `sterfjaar` int(11) DEFAULT NULL,
  `sterfplaats` varchar(255) DEFAULT NULL,
  `naam` varchar(255) DEFAULT NULL,
  `geslachtsnaam` varchar(255) DEFAULT NULL,
  `names` text,
  `sort_key` varchar(50) DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `search_source` text,
  `snippet` text,
  `remarks` text,
  `thumbnail` varchar(255) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `has_illustrations` tinyint(1) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`bioport_id`),
  UNIQUE KEY `ix_person_bioport_id` (`bioport_id`),
  KEY `ix_person_naam` (`naam`),
  KEY `ix_person_geslachtsnaam` (`geslachtsnaam`),
  KEY `ix_person_sort_key` (`sort_key`),
  KEY `ix_person_sex` (`sex`),
  KEY `ix_person_geboortedatum` (`geboortedatum`),
  KEY `ix_person_geboorteplaats` (`geboorteplaats`),
  KEY `ix_person_status` (`status`),
  KEY `ix_person_geboortejaar` (`geboortejaar`),
  KEY `ix_person_sterfdatum` (`sterfdatum`),
  KEY `ix_person_sterfjaar` (`sterfjaar`),
  KEY `ix_person_sterfplaats` (`sterfplaats`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `person` VALUES ('27201748','1893-04-22',1893,'IJsbrechtum','1976-07-22',1976,'Leiden','Boschma, Hilbrand','Boschma','Hilbrand Boschma','boschma hilbrand',1,'Hilbrand Boschma\nNone',NULL,NULL,'/thumbnails/120x100_knaw_fd2d4b60b48601669fc68820118b135f_image1.jpg',1,1,'2010-06-11 08:42:37'),('84972544','1778-03-31',1778,'Amsterdam','1858-01-30',1858,'Lisse','Boschma twee, Hilbrand','Boschma twee','Hilbrand Boschma twee','boschma twee hilbrand',1,'Hilbrand Boschma twee\nDit is een test-tekst. Dit woord Molloy staat alleen in de tekst.','Dit is een test-tekst. Dit woord Molloy staat alleen in de...',NULL,'',1,0,'2010-06-11 08:42:37'),('44333513','1888-05-17',1888,'Amsterdam','1965-11-11',1965,'Driebergen','Boschma Kraemer, Hilbrand Hendrik','Boschma Kraemer','Hilbrand Boschma\n        Hendrik Kraemer','boschma kraemer hilbrand hendrik',1,'Hilbrand Boschma\n        Hendrik Kraemer\nPOPPES, Eelkje (geb. Lemmer, Friesland, 9-2-1791 â€“ gest. Leeuwarden 20-9-1828), gelegenheidsdichteres. Dochter van Poppe Jans Poppes (1747-1810) en Antje Annes Visser (1758-1832). Op 22-6-1815 trouwde Eelkje Poppes in Lemmer met Christianus Petrus Eliza RobidÃ© van der Aa (1791-1851), advocaat, letterkundige, dichter. Uit het huwelijk werden 8 kinderen geboren, van wie 3 dochters de volwassen leeftijd bereikten. Er was wellicht ook 1 pleegzoon.Eelkje Poppes stamde uit een â€˜achtenswaardigâ€™ (Van der Aa) Fries geslacht. In 1814 verscheen van haar, autodidact in de dichtkunst, een bundeltje van drie gedichten onder de titel: Eerstelingen aan mijn vaderland, voorafgegaan door een lofdicht van haar toekomstige man. Deze patriottisch-orangistische verzen schreef zij naar aanleiding van de val van Napoleon en het vertrek van de Fransen uit Nederland eind 1813.In 1815 trouwde zij met Christianus RobidÃ© van der Aa, die toen secretaris van Lemsterland was. Het echtpaar ging in 1818 in Leeuwarden wonen en betrok daar wat tegenwoordig het Fries Letterkundig Museum en Documentatiecentrum is en waar in de jaren 1880 Margaretha Zelle, beter bekend als Mata Hari, heeft gewoond. Voorzover bekend heeft Eelkje Poppes na haar Eerstelingen nooit meer iets gepubliceerd. Wel schijnt zij nog enkele kindergedichtjes geschreven te hebben.Eelkje Poppes overleed op 20 september 1828, 37 jaar oud. De gedenksteen die haar echtgenoot liet aanbrengen in de muur van de kerk in Huizum vermeldt niet alleen haar dood maar ook die van â€˜vijf onzer kinderenâ€™. En in een vierregelig vers gedenkt hij het â€˜aards gelukâ€™ dat ze â€˜meer dan dertien jaarâ€™ deelden.NaslagwerkenVan der Aa; NBAC.ArchivaliaKoninklijke Bibliotheek, Den Haag: brieven aan Poppes van RobidÃ© van der Aa uit 1815 [sign. 129 E 29].Universiteitsbibliotheek Amsterdam (UvA), Handschriften: enkele familiedocumenten [Hss. Ce2e, Ce2f].PublicatieEerstelingen aan mijn vaderland (Sneek z.j. [1814]) [Knuttel Pflt. 23760].LiteratuurSytse ten Hoeve, \'By it portret fan Eelkje Poppes\', De Moanne 6 (2007) 6, 18-21.IllustratieOlieverfportret op paneel, anonieme kunstenaar, ca. 1800 (Particuliere collectie).Auteur: Anna de Haas','POPPES, Eelkje (geb. Lemmer, Friesland, 9-2-1791 â€“ gest. Leeuwarden 20-9-1828), gelegenheidsdichteres. Dochter van Poppe Jans Poppes (1747-1810) en Antje Annes Visser (1758-1832). Op 22-6-1815...',NULL,'/thumbnails/120x100_knaw_fd2d4b60b48601669fc68820118b135f_image2.jpg',1,1,'2010-06-11 08:42:37'),('27943051','1805-01-25',1805,'Amsterdam','1882-01-15',1882,'Amsterdam','Boschma 4 St&aacute;amkart, Hilbrand Franciscus Johannes','Boschma 4 St&aacute;amkart','Hilbrand Boschma 4\n	    Franciscus Johannes St&aacute;amkart','boschma 4 st&aacute;amkart hilbrand fran',1,'Hilbrand Boschma 4\n	    Franciscus Johannes St&aacute;amkart\nNone',NULL,NULL,'',1,0,'2010-06-11 08:42:37'),('32802206','1788-01-01',1788,'Ameide','1847-03-20',1847,NULL,'A, Arien','A','Arien A','a arien',1,'Arien A\nTER&#13;\nGEDACHTENIS\nVAN\nDR. R. C.&#13;\nBAKHUIZEN VAN DEN BRINK.\nDOOR\nI.. Pb. C. VAN DEN BF.ROH *).\nEen uitstekend lid is aan dezen kring&#13;\nontvallen, Dr. Rei&#173;nier Coenelis&#13;\nBakhuizen van den Betnk. Hij is weggemaaid in de volle kracht des&#13;\nlevens, in de volle frischheid van geest, die hem kenmerkte, maar zijne&#13;\nletterkundige en wetenschappe&#173;lijke verdiensten zullen in herinnering blijven,&#13;\nomdat hij de kwijnende letterkunde heeft opgefrischt en de wetenschap voor&#173;uit&#13;\ndoen gaan.\nToen wij na de zomervacantie het eerst&#13;\nweder hier vergader&#173;den, sprak de tijdelijke voorzitter een enkel woord ter&#13;\neere van den ontslapene en herinnerde daarbij te regt, hoe hij een der&#13;\nwerkzaamste leden der akademie geweest was, die, hetzij hij aan de discussie&#13;\nover eenig voorgedragen onderwerp deel nam, hetzij hij zijn oordeel uitbragt&#13;\nover vraagstukken in zijne han&#173;den gesteld, altijd de aandacht zijner medeleden&#13;\nbezig hield, want wat hij sprak was belangrijk van inhoud en puntig van stijl.&#13;\nMaar nooit heeft hij, mijns inziens, zoo belangrijk, zoo uitstekend gesproken,&#13;\nals toen hij zijnen geliefden leermeester Bake&#13;\nde laatste hulde toebragt. Gij herinnert het u, MHH., hoe hij allen aan&#13;\nzijne lippen boeide en dat, hoe uitvoerig dat\n*) Gelezen in de vergadering der&#13;\nKoninkl. Akad.&#160; van Wetenschappen, den&#13;\n18den November 1865.\nJaarbokk 1866.&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160; 1\n\n\n\n\n\r\n \r\n( 2 )\nstuk ook was, niemand het te lang vond. Dat was&#13;\nzijn zwa&#173;nenzang. Slechts een jaar daarna wordt ook hij hier herdacht en het&#13;\ntafereel van zyn leven e&#187; werken volgt op dat van zij&#173;nen leermeester.\nHet werd mij opgedragen dat tafereel te&#13;\nschetsen. Ik heb lang geaarzeld eer ik die moeijelijke taak aanvaardde, waut&#13;\nmijne betrekking tot den overledene dagteekent slechts van zijne plaatsing aan&#13;\nhet rijksarchief of weinig eerder. Van zijn vroe&#173;ger veelbewogen leven, van&#13;\nzijn werken en schrijven was mij slechts een gedeelte, en dat nog onvolledig,&#13;\nbekend en eene poging om inlichtingen te verkrijgen, bij een zijner vroegere&#13;\nmedearbeiders op het veld der letterkunde aangewend, werd afgewezen. Maar toen&#13;\nieder zijner vrienden zich van die. taak verschoonde, meende ik verpligt te&#13;\nzijn ook met gebrekkige hulpmiddelen op te treden, omdat ik vooral wenschte,&#13;\ndat zijne groote verdiensten omtrent het&#13;\narchiefwezen algemeen bekend en erkend worden en niemand zoo naauwkeurig&#13;\ndaarvan berigt kon geven als zijn veeljarige vriend en medearbeider, die meer&#13;\ndan twaalf jaren dagelijks met hem daaraan zijne krachten gewijd heeft Die&#13;\nbeweegreden moge het gebrekkige van den vorm en het onvolledige van den inhoud&#13;\nverschoonen.\nEr zijn velen, wier biograaph zorgvuldig&#13;\nalle gebreken be-mantelen en daarentegen elke goede zijde helder moet doen&#13;\nuitkomen, wil hij bij den lezer of hoorder nog eenige belang&#173;stelling voor&#13;\nzijnen held opwekken. Dat is het geval met de meesten, voor wie jaarlijks in de&#13;\ngenootschappen de doodklok geluid wordt; maar er zijn ook enkelen, wier&#13;\ngebreken men on&#173;bevreesd erkennen mag, omdat er meer voortreffelijk&#187; tegenover&#13;\nstaat, en zij ook met die menschelijke zwakheden een belangrijk leven geleefd&#13;\nhebben.&#160;&#160;&#160; Tot die weinigen behoorde Bakhuizen.\nHij was een volbloed Amsterdammer, zoowel&#13;\nvan afkomst als van genegenheid. Geboren den 288ten Februari] 1810,&#13;\ngenoot hij aan het gymnasium dezer stad zijne eerste opleiding tot de&#13;\nwetenschap, onder den toenmaligen rector Zilubskn.&#13;\nDaarop hoorde hij de lessen aan het athenaeum, bestemd, hetzij dan door&#13;\nzijne ouders of naar eigene keus, voor de theologie. Maar om tot dat heiligdom&#13;\nin te gaan, moest hij eerst door den aan-\n\n\n\n\n\r\n \r\n(3)\nlokkenden tuin der philologie en daar boeide hem vooral de smaakvolle&#13;\nvoordragt van den hoogleeraar van&#13;\nLennkp. Nog in lateren tijd gewaagde hij dikwijls met welgevallen van&#13;\nhet&#173;geen hij van dezen gehoord had en hij heeft dan ook bij diens overlijden&#13;\nzijn aandenken dankbaar gevierd in een artikel, op&#173;genomen in het tijdschrift de&#13;\nletterbode. Toch verwaarloosde hij daarom de studie der godgeleerdheid niet&#13;\nen hij heeft mij meermalen verklaard, dat hij inzonderheid de historia&#13;\ndogmatum met belangstelling beoefend had, waarschijnlijk geleid door zijne&#13;\ntoenmalige philosophische studi&#235;n.\nNa te Amsterdam eene poos gestudeerd te&#13;\nhebben, vertrok hij naar Leiden om daar zijne studi&#235;n te voltooijen. Hier slqeg&#13;\nhij de wieken uit: aan den eenen kant genoot hij volop de vrij&#173;heid en de&#13;\nvreugd van het studentenleven, zelfs wel eens meer dan nuttig was, maar aan den&#13;\nanderen kant zwelgde hij even&#173;zeer in de genietingen der wetenschap. Wat hij&#13;\nwas, was hij geheel en rondborstig. Dartel en overmoedig, maar goedhartig en&#13;\noorspronkelijk, was hij onder vrienden de vrolijkste, de wild&#173;ste, aan zijne&#13;\nstudeertafel de onvermoeidste. Een zijner tijdgenoo-ten aan de akademie&#13;\nverhaalde mij, dat meer dan eens, na een gloeijend studentenfeest, waar hij de&#13;\nuitgelatenste, de meest ru&#173;moerige van allen geweest was, wanneer men eindelijk&#13;\nin het holle van den nacht uiteen ging en anderen afgemat naar huis waggelden&#13;\nen op hun bed neerzonken, hij dan zijne lamp aan&#173;stak om zich in Pindarus te&#13;\nverdienen.\nToch had hij eindelijk in dat&#13;\nstudentikoose leven geheel knn-nen ondergaan, had hij niet te Leiden twee&#13;\nmannen gevonden, die als goede genii hem ter zijde stonden en die hem voor de&#13;\nwetenschap behielden, Bake en Geel. Wat hij aan den eerste te danken&#13;\nhad heeft hij zelf het vorige jaar in warme taal uit&#173;gesproken, wat de ander&#13;\nvoor hem was blijkt uit zijne brieven en&#13;\nerkent hij zelf in zijne Epistola critica ad faeobum Geelium, opgenomen&#13;\nia het vijfde deel der Sym&#232;olae litemriae. #Norunt omnes (zegt bij&#13;\ndaar), qui literarum disciplinae haud fiavavat-%incumbant, quauto&#13;\neos amplecti amore, quamque eos in sinu veluti gestare consueveris: ego vero in&#13;\npaucis haud magis te artis magistrum quam consiliorum&#160; totiusque vitae&#160; praecep-\n1*','TER&#13;\nGEDACHTENIS\nVAN\nDR. R. C.&#13;\nBAKHUIZEN VAN DEN BRINK.\nDOOR\nI.. Pb. C. VAN DEN BF.ROH *).\nEen uitstekend lid is aan dezen kring&#13;\nontvallen, Dr. Rei&#173;nier Coenelis&#13;\nBakhuizen...',NULL,'',1,0,'2010-06-11 08:42:37'),('31132281','1773-03-31',1773,'Paesens, Frankrijk','1826-02-24',1826,'Leiden','Boschma, Hilbrand Molloyx','Boschma','Hilbrand MolloyX Boschma Cornelis Ekama','boschma hilbrand molloyx',1,'Hilbrand MolloyX Boschma\nCornelis Ekama\nNone',NULL,NULL,'',1,0,'2010-06-11 08:42:37'),('15590559','1750-01-01',1750,'Gent, BelgiÃ«','1819-11-01',1819,'Gent, BelgiÃ«','Stamkart, Pierre Emmanuel','Stamkart','Pierre Emmanuel Stamkart Hilbrand Boschma','stamkart pierre emmanuel',1,'Pierre Emmanuel Stamkart\nHilbrand Boschma\nNone',NULL,NULL,'',1,0,'2010-06-11 08:42:37'),('38318174','1824-12-03',1824,'Brussel, BelgiÃ«','1904-05-15',1904,'\'s Gravenhage','MichaÃ«lis, Nicolaas Theodoor','MichaÃ«lis','Nicolaas Theodoor MichaÃ«lis Hendrik Kraemer Hilbrand Boschma twee','michaelis nicolaas theodoor',1,'Nicolaas Theodoor MichaÃ«lis\nHendrik Kraemer\nHilbrand Boschma twee\nNone',NULL,NULL,'',1,0,'2010-06-11 08:42:37'),('28104076','1892-10-28',1892,'Tilburg','1965-05-18',1965,'De Bilt','Dijksterhuis, Eduard Jan','Dijksterhuis','Eduard Jan Dijksterhuis C. van Heynsbergen Hilbrand Boschma twee','dijksterhuis eduard jan',1,'Eduard Jan Dijksterhuis\nC. van Heynsbergen\nHilbrand Boschma twee\nNone',NULL,NULL,'',1,0,'2010-06-11 08:42:37'),('75994708','1845-07-09',1845,'Down, Groot BrittaniÃ«','1912-12-07',1912,'Newham, Groot BrittaniÃ«','Darwin, George Howard','Darwin','George Howard Darwin Hilbrand Boschma','darwin george howard',1,'George Howard Darwin\nHilbrand Boschma\nNone',NULL,NULL,'',1,0,'2010-06-11 08:42:38');
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person_name`
--

DROP TABLE IF EXISTS `person_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person_name` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bioport_id` varchar(50) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_person_name_name` (`name`),
  KEY `ix_person_name_bioport_id` (`bioport_id`)
) ENGINE=MyISAM AUTO_INCREMENT=53 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person_name`
--

LOCK TABLES `person_name` WRITE;
/*!40000 ALTER TABLE `person_name` DISABLE KEYS */;
INSERT INTO `person_name` VALUES (1,'27201748','Hilbrand'),(2,'27201748','Boschma'),(3,'84972544','Hilbrand'),(4,'84972544','Boschma'),(5,'84972544','twee'),(6,'44333513','Hilbrand'),(7,'44333513','Boschma'),(8,'44333513','Hendrik'),(9,'44333513','Kraemer'),(10,'27943051','Hilbrand'),(11,'27943051','Boschma'),(12,'27943051','4'),(13,'27943051','Franciscus'),(14,'27943051','Johannes'),(15,'27943051','St'),(16,'27943051','aacute'),(17,'27943051','amkart'),(18,'32802206','Arien'),(19,'32802206','A'),(20,'31132281','Hilbrand'),(21,'31132281','MolloyX'),(22,'31132281','Boschma'),(23,'31132281','Cornelis'),(24,'31132281','Ekama'),(25,'15590559','Pierre'),(26,'15590559','Emmanuel'),(27,'15590559','Stamkart'),(28,'15590559','Hilbrand'),(29,'15590559','Boschma'),(30,'38318174','Nicolaas'),(31,'38318174','Theodoor'),(32,'38318174','Micha'),(33,'38318174','lis'),(34,'38318174','Hendrik'),(35,'38318174','Kraemer'),(36,'38318174','Hilbrand'),(37,'38318174','Boschma'),(38,'38318174','twee'),(39,'28104076','Eduard'),(40,'28104076','Jan'),(41,'28104076','Dijksterhuis'),(42,'28104076','C'),(43,'28104076','van'),(44,'28104076','Heynsbergen'),(45,'28104076','Hilbrand'),(46,'28104076','Boschma'),(47,'28104076','twee'),(48,'75994708','George'),(49,'75994708','Howard'),(50,'75994708','Darwin'),(51,'75994708','Hilbrand'),(52,'75994708','Boschma');
/*!40000 ALTER TABLE `person_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person_soundex`
--

DROP TABLE IF EXISTS `person_soundex`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person_soundex` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bioport_id` varchar(50) DEFAULT NULL,
  `soundex` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_person_soundex_soundex` (`soundex`),
  KEY `ix_person_soundex_bioport_id` (`bioport_id`)
) ENGINE=MyISAM AUTO_INCREMENT=49 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person_soundex`
--

LOCK TABLES `person_soundex` WRITE;
/*!40000 ALTER TABLE `person_soundex` DISABLE KEYS */;
INSERT INTO `person_soundex` VALUES (1,'27201748','hilbrant'),(2,'27201748','bosma'),(3,'84972544','tfe'),(4,'84972544','hilbrant'),(5,'84972544','bosma'),(6,'44333513','hendrik'),(7,'44333513','hilbrant'),(8,'44333513','bosma'),(9,'44333513','kramer'),(10,'27943051','hilbrant'),(11,'27943051','frankiskus'),(12,'27943051','amkart'),(13,'27943051','st'),(14,'27943051','joanes'),(15,'27943051','akute'),(16,'27943051','bosma'),(17,'32802206','arien'),(18,'31132281','ekama'),(19,'31132281','hilbrant'),(20,'31132281','bosma'),(21,'31132281','moloik'),(22,'31132281','kornelis'),(23,'15590559','piere'),(24,'15590559','hilbrant'),(25,'15590559','bosma'),(26,'15590559','stamkart'),(27,'15590559','emanul'),(28,'38318174','hilbrant'),(29,'38318174','tfe'),(30,'38318174','kramer'),(31,'38318174','migalis'),(32,'38318174','hendrik'),(33,'38318174','teodor'),(34,'38318174','nikolas'),(35,'38318174','bosma'),(36,'28104076','hilbrant'),(37,'28104076','hinsbergen'),(38,'28104076','tfe'),(39,'28104076','jan'),(40,'28104076','fan'),(41,'28104076','bosma'),(42,'28104076','eduart'),(43,'28104076','dikteruis'),(44,'75994708','hilbrant'),(45,'75994708','bosma'),(46,'75994708','hofart'),(47,'75994708','george'),(48,'75994708','darfin');
/*!40000 ALTER TABLE `person_soundex` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person_source`
--

DROP TABLE IF EXISTS `person_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bioport_id` varchar(50) DEFAULT NULL,
  `source_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_person_source_source_id` (`source_id`),
  KEY `ix_person_source_bioport_id` (`bioport_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person_source`
--

LOCK TABLES `person_source` WRITE;
/*!40000 ALTER TABLE `person_source` DISABLE KEYS */;
INSERT INTO `person_source` VALUES (1,'27201748','knaw'),(2,'84972544','knaw'),(3,'44333513','knaw'),(4,'27943051','knaw'),(5,'32802206','knaw'),(6,'31132281','knaw2'),(7,'15590559','knaw2'),(8,'38318174','knaw2'),(9,'28104076','knaw2'),(10,'75994708','knaw2');
/*!40000 ALTER TABLE `person_source` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relbiographyauthor`
--

DROP TABLE IF EXISTS `relbiographyauthor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relbiographyauthor` (
  `biography_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `author_id` int(11) NOT NULL,
  PRIMARY KEY (`biography_id`,`author_id`),
  KEY `author_id` (`author_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relbiographyauthor`
--

LOCK TABLES `relbiographyauthor` WRITE;
/*!40000 ALTER TABLE `relbiographyauthor` DISABLE KEYS */;
/*!40000 ALTER TABLE `relbiographyauthor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relbioportidbiography`
--

DROP TABLE IF EXISTS `relbioportidbiography`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relbioportidbiography` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bioport_id` varchar(50) DEFAULT NULL,
  `biography_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_relbioportidbiography_biography_id` (`biography_id`),
  KEY `ix_relbioportidbiography_bioport_id` (`bioport_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relbioportidbiography`
--

LOCK TABLES `relbioportidbiography` WRITE;
/*!40000 ALTER TABLE `relbioportidbiography` DISABLE KEYS */;
INSERT INTO `relbioportidbiography` VALUES (1,'27201748','knaw/001','2010-06-11 08:42:37'),(2,'84972544','knaw/002','2010-06-11 08:42:37'),(3,'44333513','knaw/003','2010-06-11 08:42:37'),(4,'27943051','knaw/004','2010-06-11 08:42:37'),(5,'32802206','knaw/005','2010-06-11 08:42:37'),(6,'31132281','knaw2/006','2010-06-11 08:42:37'),(7,'15590559','knaw2/007','2010-06-11 08:42:37'),(8,'38318174','knaw2/008','2010-06-11 08:42:37'),(9,'28104076','knaw2/00a','2010-06-11 08:42:37'),(10,'75994708','knaw2/00A','2010-06-11 08:42:38');
/*!40000 ALTER TABLE `relbioportidbiography` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relpersoncategory`
--

DROP TABLE IF EXISTS `relpersoncategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relpersoncategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bioport_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_relpersoncategory_category_id` (`category_id`),
  KEY `ix_relpersoncategory_bioport_id` (`bioport_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relpersoncategory`
--

LOCK TABLES `relpersoncategory` WRITE;
/*!40000 ALTER TABLE `relpersoncategory` DISABLE KEYS */;
INSERT INTO `relpersoncategory` VALUES (1,84972544,1);
/*!40000 ALTER TABLE `relpersoncategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `soundex`
--

DROP TABLE IF EXISTS `soundex`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `soundex` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `naam_id` int(11) DEFAULT NULL,
  `soundex` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `naam_id` (`naam_id`)
) ENGINE=MyISAM AUTO_INCREMENT=48 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `soundex`
--

LOCK TABLES `soundex` WRITE;
/*!40000 ALTER TABLE `soundex` DISABLE KEYS */;
INSERT INTO `soundex` VALUES (1,1,'.lpr'),(2,1,'p.sn'),(3,2,'tf'),(4,2,'p.sn'),(5,2,'.lpr'),(6,3,'.lpr'),(7,3,'p.sn'),(8,3,'.ntr'),(9,3,'kr.n'),(10,4,'fr.n'),(11,4,'j.h.'),(12,4,'st'),(13,4,'.lpr'),(14,4,'p.sn'),(15,4,'.k.t'),(16,4,'.nk.'),(17,5,'.r'),(18,6,'.lpr'),(19,6,'p.sn'),(20,6,'n.l.'),(21,7,'.k.n'),(22,7,'k.rn'),(23,8,'st.n'),(24,8,'p.r'),(25,8,'.n.n'),(26,9,'.lpr'),(27,9,'p.sn'),(28,10,'n.g.'),(29,10,'th.t'),(30,10,'n.k.'),(31,11,'.ntr'),(32,11,'kr.n'),(33,12,'tf'),(34,12,'p.sn'),(35,12,'.lpr'),(36,13,'t.ks'),(37,13,'.t.r'),(38,13,'j.n'),(39,14,'.nsp'),(40,15,'tf'),(41,15,'p.sn'),(42,15,'.lpr'),(43,16,'.f.r'),(44,16,'g.rg'),(45,16,'t.rf'),(46,17,'.lpr'),(47,17,'p.sn');
/*!40000 ALTER TABLE `soundex` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `source`
--

DROP TABLE IF EXISTS `source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `source` (
  `id` varchar(50) NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `quality` int(11) DEFAULT NULL,
  `xml` text,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_source_id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `source`
--

LOCK TABLES `source` WRITE;
/*!40000 ALTER TABLE `source` DISABLE KEYS */;
INSERT INTO `source` VALUES ('knaw','file:///home/jelle/projects_active/bioport/site/parts/Products/BioPortRepository/tests/data/knaw/list.xml','test',NULL,'<biodes_source>\n  <id>knaw</id>\n  <url>file:///home/jelle/projects_active/bioport/site/parts/Products/BioPortRepository/tests/data/knaw/list.xml</url>\n  <description>test</description>\n  <quality>0</quality>\n  <default_status>1</default_status>\n</biodes_source>\n','2010-06-11 08:42:37'),('knaw2','file:///home/jelle/projects_active/bioport/site/parts/Products/BioPortRepository/tests/data/knaw2/list.xml','test',NULL,'<biodes_source>\n  <id>knaw2</id>\n  <url>file:///home/jelle/projects_active/bioport/site/parts/Products/BioPortRepository/tests/data/knaw2/list.xml</url>\n  <description>test</description>\n  <quality>0</quality>\n  <default_status>1</default_status>\n</biodes_source>\n','2010-06-11 08:42:37');
/*!40000 ALTER TABLE `source` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-06-11 10:42:38
