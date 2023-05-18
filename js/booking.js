import { html } from "./vendor.js";

function GazeboRow({ id, title, subTitle, date, scheduleOptions }) {
  return html`<tr>
    <th>
      ${title}
      <p class="description">${subTitle}</p>
    </th>
    ${scheduleOptions.map((scheduleOption) => {
      if (!scheduleOption) return html`<td class="center">-</td>`;

      const selectScheduleOption = () => {
        Telegram.WebApp.showConfirm(
          `Забронювати ${title} на ${date} з ${scheduleOption.textFrom} по ${scheduleOption.textTo}?`,
          (confirmed) => {
            if (!confirmed) return;

            Telegram.WebApp.sendData(
              JSON.stringify({
                gazeboId: id,
                date,
                scheduleOptionIdx: scheduleOption.idx,
              })
            );
          }
        );
      };

      return html`<td class="center">
        <a class="button button-outline" onClick=${selectScheduleOption}>
          ${scheduleOption.textFrom}
          <br />
          ${scheduleOption.textTo}
        </a>
      </td>`;
    })}
  </tr>`;
}

function parseInputState() {
  const params = new URLSearchParams(window.location.search);
  const encodedState = params.get("s");
  return JSON.parse(encodedState);
}

export function BookingTable() {
  const state = parseInputState();

  const gazebos = state.gazebos.map((option) => {
    return {
      id: option[0],
      title: option[1],
      subTitle: option[2],
      date: state.date,
      scheduleOptions: option[3].map((isAvailable, idx) =>
        isAvailable
          ? {
              idx,
              textFrom: state.schedules[idx][0],
              textTo: state.schedules[idx][1],
            }
          : null
      ),
    };
  });

  return html`<h6 class="center no-margin">Бронювання на ${state.date}</h3>
    <table>
      <tbody>
        ${gazebos.map((gazebo) => GazeboRow(gazebo))}
      </tbody>
    </table>`;
}
