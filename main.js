import { html, render } from "./js/vendor.js";
import { BookingTable } from "./js/booking.js";
import { initEvents } from "./js/events.js";

initEvents();

render(html`<${BookingTable} />`, document.getElementById("booking-table"));

Telegram.WebApp.expand();
Telegram.WebApp.ready();
