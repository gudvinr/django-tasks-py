var submitForm = document.querySelector('form');        // Form used to submit new task and new roadmap
var switchInput = submitForm.querySelector('.switch');  // Switch element of task view used to change task state
var delBtn = document.getElementById('delete_btn');     // Button to delete roadmap/task

submitForm.addEventListener('input', checkInput);

// Make submit button enabled if all fields are filled
function checkInput() {
    if (switchInput && switchInput.querySelector('input').checked) return;

    var btn = submitForm.querySelector('#submit_btn');

    var inputs = submitForm.querySelectorAll('input');
    for (var i = 0; i < inputs.length; i++) if (!inputs[i].checkValidity()) return;

    if (!$('.datepicker').pickadate('get', 'select')) return;

    if (btn.classList.contains('disabled')) btn.classList.remove('disabled');
}

// Send delete request to server and redirect to parent view
if (delBtn) delBtn.addEventListener('click', function (event) {
    if (event) event.preventDefault();

    var url = window.location.href;
    var redirUrl = (event.target && event.target.href) ? event.target.href : window.location.origin;

    var del = new XMLHttpRequest();

    del.addEventListener('load', function (event) {
        var resp = JSON.parse(event.target.response);

        if (resp && resp.ok) window.location = redirUrl;
        else handleError(event, null);
    });

    del.addEventListener('error', handleError);
    del.addEventListener('abort', handleError);

    del.open('DELETE', url);
    del.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    del.send();
})

// Submit form on ready switch toggle
if (switchInput) switchInput.addEventListener('click', function (event) {
    var cb = switchInput.querySelector('input');

    if (cb.checked && !cb.disabled) {
        var inputs = submitForm.querySelectorAll('input');

        sendForm();

        for (var i = 0; i < inputs.length; i++) inputs[i].disabled = true;
    }
})

submitForm.addEventListener('submit', sendForm)

// Submit form data and append child on success
function sendForm(event) {
    if (event) event.preventDefault();

    var btn = submitForm.querySelector('#submit_btn');
    if (!btn.classList.contains('disabled')) btn.classList.add('disabled');

    var post = new XMLHttpRequest();

    post.addEventListener('load', function (event) {
        var resp = JSON.parse(event.target.response);

        if (resp && resp.ok) {
            resp = resp.result;

            var list = document.querySelector('.collection');

            // If roadmap or roadmap list append received item
            if (list) {
                var child = document.createElement('a');
                child.href = resp._url;
                child.innerText = resp.title;
                child.classList.add(
                    "collection-item", "light-blue-text", "text-darken-4",
                    "scale-transition", "scale-out"
                );

                list.appendChild(child);

                setTimeout(function () {
                    child.classList.remove("scale-out");
                }, 0);
            }

            Materialize.toast(list ? 'Added: ' + resp.title : 'Edited');
        } else
            handleError(event, btn)
    });

    post.addEventListener('error', function (event) { handleError(event, btn) });
    post.addEventListener('abort', function (event) { handleError(event, btn) });

    post.open('POST', submitForm.action)
    post.send(new FormData(submitForm));
}

// Print errors
function handleError(event, btn) {
    var resp;
    if (event && event.target) resp = JSON.parse(event.target.response);

    console.log(resp);

    var err = '<div>Error: ' + ((resp && resp.error) ? resp.error + '</div>' : 'undefined</div>');

    Materialize.toast(err, 5000);
    if (btn && btn.classList.contains('disabled')) btn.classList.remove('disabled');
}

function loadStat(url) {
    var get = new XMLHttpRequest();

    get.addEventListener('load', function (event) {
        var resp = JSON.parse(event.target.response);

        if (resp && resp.ok) {
            resp = resp.result;

            var weeklyStat = document.getElementById('weekly_stat');
            for (var i = 0; i < resp.weekly.length; i++) {
                var elem = document.createElement('tr');
                elem.innerHTML = '<td>' + resp.weekly[i].week + '</td>';
                elem.innerHTML += '<td>' + resp.weekly[i].year + '</td>';
                elem.innerHTML += '<td>' + resp.weekly[i].total + '</td>';
                elem.innerHTML += '<td>' + resp.weekly[i].done + '</td>';

                weeklyStat.appendChild(elem);
            }

            var monthlyStat = document.getElementById('monthly_stat');
            for (var i = 0; i < resp.monthly.length; i++) {
                var elem = document.createElement('tr');
                elem.innerHTML = '<td>' + resp.monthly[i].month + '</td>';
                elem.innerHTML += '<td>' + resp.monthly[i].scores + '</td>';

                monthlyStat.appendChild(elem);
            }

            drawCharts(resp);
        }
        else
            handleError(event);
    });

    get.addEventListener('error', function (event) { handleError(event) });
    get.addEventListener('abort', function (event) { handleError(event) });

    get.open('GET', url);
    get.send();
}

function drawCharts(data) {
    var weeklyChart = new Chart('weekly_chart', {
        type: 'bar',
        data: {
            labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    var monthlyChart = new Chart('monthly_chart', {
        type: 'bar',
        data: {
            labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

// Simple method to parse cookies
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}
