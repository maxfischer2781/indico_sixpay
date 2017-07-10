# Indico EPayment plugin for SIX Payment Services

Plugin for Indico EPayment, enabling support for SIX Payment service.
This enables EPayment using the SIX Payment Service in conferences and other events.

## EPayment Configuration Settings

The Plugin can be activated and configured for each event.
This is done in the `Mod of Payments` section of `Management Area` -> `Registration` -> `e-payment`.
Once enabled, the Plugin supports the following per-event settings:

* **Title**

  Name of the service presented to users when selecting a payment provider.

* **SixPay Saferpay URL**

  The URL to contact the Six Payment Service.
  Use the default `https://www.saferpay.com/hosting` for any transaction.
  For testing, use the `https://test.saferpay.com/hosting` test service.

  You should generally not change this other than for testing.
  If the official saferpay URL changes, please submit a [ticket](https://github.com/maxfischer2781/indico_sixpay/pulls).
  
* **Account ID**

  The ID of your Saferpay account.
  For testing, use the ID `401860-17795278`.

  This ID is provided to you by Saferpay.

* **Order Description**

  The description of each order in a human readable way.
  This description is presented to the registrant during the transaction with SixPay.

  This field is limited to 50 characters, after any placeholders are filled in.
  The default description uses the registrant name and event title.

* **Order Identifier**

  The identifier of each order for further processing.

  This field is stripped of whitespace and limited to 80 characters, after any placeholders are filled in.
  Note that auxiliary services, e.g. for billing, may limit this information to 12 characters.

* **Notification Mail**

  Mail address to receive notifications of transactions.
  This is independent of Indico's own payment notifications.

### Format Placeholders

The **Order Description/Identifier** settings allow for placeholders.
These are dynamically filled for each event and registrant.

* **%(user_id)d** [`231`]

  Numerical identifier of the user/registrant, unique per event.

* **%(user_name)s** [`Jane Doe`]

  Full name of the user/registrant.

* **%(user_firstname)s** [`Jane`]

  First name of the user/registrant.

* **%(user_lastname)s** [`Doe`]

  Last name of the user/registrant.

* **%(event_id)d** [`18`]

  Numerical identifier of the event.

* **%(event_title)s** [`My Conference`]

  Full title of the event.

* **%(eventuser_id)s** [`c18r231`]

  A globally unique identifier for both the event and user.

Placeholders use the [String Formatting](https://docs.python.org/2/library/stdtypes.html#string-formatting) rules of python.
For example, the placeholder `%(event_title).6s` is replaced with the first six characters of the event title.

## Installation

The plugin can be installed using standard Python package managers.
Note that at least `indico` 1.2 is required, and will be installed if it is missing.

**Note**: The `indico_sixpay` plugin must be installed for the python version running `indico`.

### Release Version

The latest release version is available for the default python package managers.
You can directly install the module using `pip`:

    pip install indico_sixpay

This can also be used to upgrade to a newer version:

    pip install indico_sixpay --upgrade

### Latest Version

Download this repository to any host running indico.
Install it by running:

    python setup.py install

After reloading the EPayment plugin in the Indico Admin panel, you can enable the SixPay service.

## Contributing, Feedback and Bug Reports

This project is hosted on [github](https://github.com/maxfischer2781/indico_sixpay).
If you encounter any bugs or missing features, please use the [bug tracker](https://github.com/maxfischer2781/indico_sixpay/issues) or submit a [pull request](https://github.com/maxfischer2781/indico_sixpay/pulls).

### Changelog

* **v1.2.2**

    * Internal description of payments is configurable.

    * Added additional formatting placeholders for payment descriptions.

* **v1.2.1**

    Initial release

## Disclaimer

This plugin is in no way endorsed, supported or provided by SIX, Indico, KIT or any other service, provider or entity.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
