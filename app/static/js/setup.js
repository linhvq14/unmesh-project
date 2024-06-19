$(document).ready(function () {
    const $createDeviceOutput = $('#createDeviceOutput');
    const $startServicesOutput = $('#startServicesOutput');
    const $stopServicesOutput = $('#stopServicesOutput');
    const $changeSpeedOutput = $('#changeSpeedOutput');
    const $cronOutput = $('#cronOutput');

    // Show the correct container when a button is clicked
    $('#createDeviceButton').on('click', function () {
        $('.actionContainer').hide();
        $('#createDeviceContainer').show();
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

    // Run start services script
    $('#runStartServices').on('click', function () {
        $startServicesOutput.text('Starting services...');

        $.ajax({
            url: '/run_script',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ script_name: 'start_all_processes.sh' }),
            success: function (data) {
                $startServicesOutput.text(data.error ? 'Error: ' + data.error : data.output);
            },
            error: function (error) {
                $startServicesOutput.text('An error occurred: ' + error.statusText);
            }
        });
    });

    // Run stop services script
    $('#runStopServices').on('click', function () {
        $stopServicesOutput.text('Stopping services...');

        $.ajax({
            url: '/run_script',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ script_name: 'stop_all_processes.sh' }),
            success: function (data) {
                $stopServicesOutput.text(data.error ? 'Error: ' + data.error : data.output);
            },
            error: function (error) {
                $stopServicesOutput.text('An error occurred: ' + error.statusText);
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
            data: JSON.stringify({ scriptPath, cronTime }),
            success: function (data) {
                $cronOutput.text(data.message);
            },
            error: function (error) {
                $cronOutput.text('An error occurred: ' + error.statusText);
            }
        });
    });
});
