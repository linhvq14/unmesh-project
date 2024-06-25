$(document).ready(function () {
    const $startServicesOutput = $('#startServicesOutput');
    const $stopServicesOutput = $('#stopServicesOutput');
    const $connectWifiOutput = $('#connectWifiOutput');
    const $cronOutput = $('#cronOutput');
    const $initialHandshakeOutput = $('#initialHandshakeOutput');

    function getCurrentTimestamp() {
        const now = new Date();
        return now.toLocaleString();
    }

    function appendOutput($element, message) {
        const timestamp = getCurrentTimestamp();
        $element.append(`<div>[${timestamp}] ${message}</div>`);
    }

    // Show the correct container when a button is clicked
    $('#createDeviceButton').on('click', function () {
        $('.actionContainer').hide();
        $('#createDeviceContainer').show();
    });

    $('#initialHandshakeButton').on('click', function () {
        $('.actionContainer').hide();
        $('#initialHandshakeContainer').show();
    });

    $('#startServicesButton').on('click', function () {
        $('.actionContainer').hide();
        $('#startServicesContainer').show();
    });

    $('#stopServicesButton').on('click', function () {
        $('.actionContainer').hide();
        $('#stopServicesContainer').show();
    });

    $('#changeSpeedButton').on('click', function () {
        $('.actionContainer').hide();
        $('#changeSpeedContainer').show();
    });

    $('#createCronButton').on('click', function () {
        $('.actionContainer').hide();
        $('#createCronContainer').show();
    });

    $('#connectWifiButton').on('click', function () {
        $('.actionContainer').hide();
        $('#connectWifiContainer').show();
    });

    // Run start services script
    $('#runStartServices').on('click', function () {
        appendOutput($startServicesOutput, 'Starting services...');

        $.ajax({
            url: '/run_script',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({script_name: 'start_all_processes.sh'}),
            success: function (data) {
                appendOutput($startServicesOutput, data.error ? 'Error: ' + data.error : data.output);
            },
            error: function (error) {
                appendOutput($startServicesOutput, 'An error occurred: ' + error.statusText);
            }
        });
    });

    // Run stop services script
    $('#runStopServices').on('click', function () {
        appendOutput($stopServicesOutput, 'Stopping services...');

        $.ajax({
            url: '/run_script',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({script_name: 'stop_all_processes.sh'}),
            success: function (data) {
                appendOutput($stopServicesOutput, data.error ? 'Error: ' + data.error : data.output);
            },
            error: function (error) {
                appendOutput($stopServicesOutput, 'An error occurred: ' + error.statusText);
            }
        });
    });

    // Handle cron job creation
    $('#cronJobForm').submit(function (event) {
        event.preventDefault();
        const scriptPath = $('#scriptPath').val();
        const cronTime = $('#cronTime').val();

        $.ajax({
            url: '/create_cron_job',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({scriptPath, cronTime}),
            success: function (data) {
                appendOutput($cronOutput, data.message);
            },
            error: function (error) {
                appendOutput($cronOutput, 'An error occurred: ' + error.statusText);
            }
        });
    });

    // Handle change speed
    $('#changeSpeedForm').submit(function (event) {
        event.preventDefault();
        const newSpeed = $('#speedValue').val();
        if (newSpeed === "") {
            alert("Please enter a speed value.");
            return;
        }

        $.ajax({
            url: '/change_speed',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({speed: newSpeed}),
            success: function (response) {
                alert(response.message);
            },
            error: function (xhr, status, error) {
                var err = JSON.parse(xhr.responseText);
                alert(err.error);
            }
        });
    });

    // Handle connect to Wi-Fi
    $('#connectWifiForm').submit(function (event) {
        event.preventDefault();
        const ssid = $('#ssid').val();
        const password = $('#password').val();

        $.ajax({
            url: '/connect_wifi',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ssid: ssid, password: password}),
            success: function (data) {
                appendOutput($connectWifiOutput, data.message);
            },
            error: function (error) {
                appendOutput($connectWifiOutput, 'An error occurred: ' + error.statusText);
            }
        });
    });

    // Handle create device
    $('#createDeviceForm').submit(function (event) {
        event.preventDefault();
        const deviceId = $('#deviceId').val();
        if (deviceId === "") {
            alert("Please enter a Device ID value.");
            return;
        }

        $.ajax({
            url: '/create_device',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({device_id: deviceId}),
            success: function (response) {
                alert(response.message);
            },
            error: function (xhr, status, error) {
                var err = JSON.parse(xhr.responseText);
                alert(err.error);
            }
        });
    });

    // Handle initial handshake
    $('#runInitialHandshake').on('click', function () {
        appendOutput($initialHandshakeOutput, 'Running initial handshake...');

        $.ajax({
            url: '/init_handshake',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({}),
            success: function (data) {
                appendOutput($initialHandshakeOutput, data.message);
            },
            error: function (error) {
                debugger
                appendOutput($initialHandshakeOutput, 'An error occurred: ' + error.responseJSON.message);
            }
        });
    });
});
