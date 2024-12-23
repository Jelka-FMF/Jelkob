��    -      �  =   �      �  *  �               "  �  *     �  -   �  Q   	     l	  -   t	     �	     �	  L   �	     
     
    %
  #  D  6  h  
  �  �   �     �     �     �     �  $   �     �  %   �  
   �                 g   5     �  "   �  E   �  w   
  �   �  �   [     <     A  m   S  &   �  i   �  :   R  v  �  �       �     �     �  �  �     �  (   �  I   �       *        I  
   ]  A   h     �     �  0  �     �  �   �    �          !     "!     *!     1!  #   9!     ]!  "   d!     �!     �!     �!      �!  j   �!     *"  $   2"  2   W"  n   �"  �   �"  �   �#     {$     �$  n   �$     %  ^   %  ?   |%     !                ,                  +   "      %             
         -                   *         	                    (             '         $                                     #           )       &        <a href="https://github.com/Jelka-FMF/Jelkob" target="_blank">Jelkob</a> is our main server, on which we run the website, the Docker register and where the pattern database is stored. Hardware-wise, the comunication with the LED lights on the tree is done via a Raspberry Pi (code itself can be found in the <a href="https://github.com/Jelka-FMF/Korenine">Korenine</a> repository). Using that we ping the server every 30 seconds to check what is the list of patterns and downloads from the Docker register. Then it rotates through the list of enabled patterns. Each patteren is run by running a Docker container and reading what it writes to standard output. Using a library it controls the lights based on this output and sends the current state to the server, so it shows up on the simulation on the website. About About Jelka FMF Actions At the <a href="https://www.fmf.uni-lj.si/" target="_blank">Faculty of Mathematics and Physics, University of Ljubljana</a>, as part of the <a href="https://programerski-klub-fmf.github.io/" target="_blank">FMF Programming Club</a>, we set up a programmable Christmas tree. The project was made possible with the sponsorship of <a href="https://abelium.si/" target="_blank">Abelium</a> and <a href="https://acex.si/" target="_blank">Acex</a>. Author Basic information about the Jelka FMF project Christmas tree at the Faculty of Mathematics and Physics, University of Ljubljana Contact Contact information for the Jelka FMF project Contributing Patterns Disable Displaying the patterns requires JavaScript to be enabled. Please enable it. Enable How Jelkly works If you are a student and have questions about the project or would like to contact people involved in the project, you can join the <a href="https://discord.gg/ccg4nKVR44" target="_blank">FMF Programming Club Discord server</a> and ask your questions in the <code>#jelka</code> channel. If you do not have a Discord account, or are a teacher at a school that is participating or would like to participate in the project, you can contact the project's coordinator, <a href="https://www.fmf.uni-lj.si/en/directory/742/bercic-katja/" target="_blank">Assist. Dr. Katja Berčič</a>. If you would like to contribute your own pattern for running on Jelka FMF and already have programming knowledge, please check out the <a href="https://github.com/Jelka-FMF/Storzi" target="_blank">Storži</a> repository that contains already-existing patterns and instructions for submitting your own patterns. If you would like to submit a pattern but do not have programming knowledge yet, you can check out <a href="https://jelkly.fmf.uni-lj.si/docs" target="_blank">Jelkly</a>, a Scratch-like visual programming tool for creating and submitting your own Jelka FMF patterns. Jelka is written mostly in Python, while the website and Jelkly are written in JavaScript. Patterns can be written in any programming language that can be run in a Docker container and supports writing to the standard output. Language Log In Log Out Login Login page for the Jelka FMF project Logout Logout page for the Jelka FMF project Management Name Patterns Please log in to see this page. Read more about the tree or contribute your own patterns on <a href="%(about_url)s">the about page</a>. Run Some technical details about Jelka The Christmas tree is currently sleeping. Visit us when it is active. The Christmas tree is running. Visit us and view it at the Faculty of Mathematics and Physics, University of Ljubljana. The tree is located at the entrance of the building at <a href="https://www.google.si/maps/place/Jadranska+ulica+21,+1000+Ljubljana" target="_blank">Jadranska 21</a> and is lit from morning until the building closes. The website is written in Django and uses the Django REST framework for the API. Using the website we can controll exactly which patterns are running on the tree, along with enabling/disabling them and manually running them. Time Toggle navigation You can check the project's source code on <a href="https://github.com/Jelka-FMF" target="_blank">GitHub</a>. You have been logged out successfully. Your account doesn't have access to this page. To proceed, please log in with an account that has access. Your username and password didn't match. Please try again. Project-Id-Version: PACKAGE VERSION
Report-Msgid-Bugs-To: 
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language-Team: LANGUAGE <LL@li.org>
Language: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=4; plural=(n%100==1 ? 0 : n%100==2 ? 1 : n%100==3 || n%100==4 ? 2 : 3);
 <a href="https://github.com/Jelka-FMF/Jelkob" target="_blank">Jelkob</a> je glavni strežnik, na katerem je spletna stran, Docker register ter baza vzorcev. Lučke fizično upravljamo z Raspberry Pijem s kodo, ki jo najdete na repozitoriju <a href="https://github.com/Jelka-FMF/Korenine">Korenine</a>. Korenine vsakih 30 sekund vprašajo Jelkoba kakšen je seznam odobrenih vzorcev in te vzoce prenese iz Docker registra in jih ciklično menjava. Posamezen vzorec zažene tako, da zažene njegov Docker container in gleda kaj ta piše na standardni izhod. Nato s pomočjo knjižnice glede na izhod kontrolira lučke, sproti pa strežniku pošilja stanje, da se vzorec prikazuje na simulaciji na spletni strani. Informacije O Jelki FMF Dejanja Na <a href="https://www.fmf.uni-lj.si/" target="_blank">Fakulteti za matematiko in fiziko Univerze v Ljubljani</a> smo v okviru <a href="https://programerski-klub-fmf.github.io/" target="_blank">Programerskega kluba FMF</a> postavili jelko z lučkami, ki jih lahko programiramo. Projekt poteka pod sponzorstvom podjetij <a href="https://abelium.si/" target="_blank">Abelium</a> in <a href="https://acex.si/" target="_blank">Acex</a>. Avtor Osnovne informacije o projektu Jelka FMF Novoletna jelka na Fakulteti za matematiko in fiziko Univerze v Ljubljani Kontakt Kontaktne informacije za projekt Jelka FMF Prispevanje vzorcev Onemogoči Za prikaz vzorcev je potreben JavaScript. Prosimo, omogočite ga. Omogoči Kako deluje Jelkly Če ste dijak ali študent in imate vprašanja o projektu ali bi se radi povezali z ljudmi, ki so vključeni v projekt, se lahko pridružite <a href="https://discord.gg/ccg4nKVR44" target="_blank">Discord strežniku Programerskega kluba FMF</a> in svoja vprašanja zastavite v kanalu <code>#jelka</code>. Če nimate Discord računa ali ste učitelj na šoli, ki sodeluje ali bi rada sodelovala v projektu, se lahko obrnete na koordinatorico projekta, <a href="https://www.fmf.uni-lj.si/sl/imenik/742/bercic-katja/" target="_blank">asist. dr. Katjo Berčič</a>. Če želite prispevati svoj vzorec za Jelko FMF in že imate znanje programiranja, si oglejte repozitorij <a href="https://github.com/Jelka-FMF/Storzi" target="_blank">Storži</a>, ki vsebuje že obstoječe vzorce in navodila za oddajo lastnih vzorcev. Če želite oddati vzorec, ampak še nimate znanja programiranja, si oglejte <a href="https://jelkly.fmf.uni-lj.si/docs" target="_blank">Jelkly</a>, Scratchu podobno orodje za vizualno programiranje, s katerim lahko enostavno ustvarite in oddate svoje vzorce za Jelko FMF. Jelka je večinoma napisana v Pythonu, določene stvari pa so tudi v drugih jezikih (recimo spletna stran in Jelkly v JavaScriptu). Vzorci so lahko napisani v kateremkoli programskem jeziku, ki ga je mogoče zapakirati v Docker container in podpira pisanje na standardni izhod. Jezik Prijava Odjava Prijava Prijavna stran za projekt Jelka FMF Odjava Odjavna stran za projekt Jelka FMF Upravljanje Ime Vzorci Za ogled te strani se prijavite. Preberite več o jelki ali prispevajte svoje vzorce na <a href="%(about_url)s">strani z informacijami</a>. Zaženi Nekaj tehničnih podrobnosti o Jelki Jelka trenutno spi. Obiščite nas, ko je aktivna. Jelka je prižgana. Obiščite nas in si jo oglejte na Fakulteti za matematiko in fiziko Univerze v Ljubljani. Jelka stoji pri vhodu v stavbo na <a href="https://www.google.si/maps/place/Jadranska+ulica+21,+1000+Ljubljana" target="_blank">Jadranski 21</a> in je prižgana od jutra do zaprtja stavbe. Spletna stran je napisana v Djangu in z uporabo DJANGO REST ogrodja za API. S spletno stranjo lahko upravljamo jelko in določimo natanko kateri vzorec je trenutno na jelki ter jih o(ne)mogočamo. Čas Preklopi navigacijo Izvorno kodo projekta si lahko ogledate na <a href="https://github.com/Jelka-FMF" target="_blank">GitHubu</a>. Uspešno ste se odjavili. Vaš račun nima dostopa do te strani. Za nadaljevanje se prijavite z računom, ki ima dostop. Vaše uporabniško ime in geslo se ne ujemata. Poskusite znova. 