The snippet of code to run recent donation list:

    <div id="last_donations">
      Ostatnie darowizny:
      <table>
      {% for donation in campaign.list_last_donations %}
      <tr>
        <td id="donation_date">{{ donation.date_plain }}</td>
        <td id="donation_amount">{{ donation.amount_in_currency_units }} PLN</td>
      </tr>
      {% endfor %}
      </table>
    </div>
