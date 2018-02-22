## The Url  Resolver app

## Usage

Given a document symbol, append the symbol to the URL, e.g. symbol/A/C.1/72/L.4 or 
symbol/A/RES/72/29.  The default language is English but the user may add another default:

    symbol/A/RES/72/29?lang=ar for Arabic
    symbol/A/RES/72/29?lang=zh for Chinese
    symbol/A/RES/72/29?lang=fr for French
    symbol/A/RES/72/29?lang=ru for Russian
    symbol/A/RES/72/29?lang=es for Spanish
    symbol/A/RES/72/29?lang=de for German

(Please note, not all documents are availble in all languages.)

Or the user can click on the language he or she wants to view.

There is a link to the original document on the United Nations Digial Library site
just right of the language boxes -- this brings up a modal that allows the user to copy and
paste the link into a seperate tab or window.  Just below the language buttons is
the document symbol and a link to the UNDL page for that symbol.

Clicking on the `Metdata` tab brings the user to the most relevant metadata for the document.

Each metadata section (Summary, Agenda, Subjects, etc) has an orange button that opens
a modal with a link to that section's metadata.

At the top of the page, just below the metadata banner is a blue button for `All Metadata`.

The link to the metadata can be copy and pasted into another window or tab.

Opening the link to metadata presents JSON.  There is an XML button at the bottom.


**Setup**
create a virtual environment on your local machine:
* virtualenv -p path_to_python3_binary envname
* source envname
* pip install -r requirements.txt

**Running locally**
for local setup there is a helper script: start.sh

**Deployment**
TBD
