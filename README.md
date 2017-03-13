# Indico EPayment plugin for SIX Payment Services

Plugin for Indico EPayment, enabling support for SIX Payment service.
This enables EPayment using the SIX Payment Service in conferences and other events.

## Installation

Download this repository to any host running indico.
Install it by running

    python setup.py install

After reloading the EPayment plugin in the Indico Admin panel, you can enable the SixPay service.

## Module Settings

This Plugin supports the following per-event settings:

* **Title**

  Name of the service presented to users when selecting a payment provider.
  
* **SixPay Saferpay URL**

  The URL to contact the Six Payment Service.
  Use the default `https://www.saferpay.com/hosting` for any transaction.
  For testing, use the `https://test.saferpay.com/hosting` test service.
  
* **Account ID**

  The ID of your Saferpay account.
  For testing, use the ID `401860-17795278`.

* **Registrant Transaction Description**

  The name of the transaction presented to the registrant during the transaction with SixPay.
  
* **Notification Mail Address**

  Mail address to receive notifications of transactions.
  This is independent of Indico's own payment notifications.

## Disclaimer

This plugin is in no way endorsed, supported or provided by SIX, Indico or any other service, provider or entity.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
