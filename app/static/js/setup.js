$(document).ready(function () {
    const $output = $('#output');
    const $cronOutput = $('#cronOutput');

    $('#runScriptButton').on('click', function () {
        const selectedScript = $('#scriptSelect').val();
        $output.text('Running script...');

        $.ajax({
            url: '/run_script',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ script_name: selectedScript }),
            success: function (data) {
                $output.text(data.error ? 'Error: ' + data.error : data.output);
            },
            error: function (error) {
                $output.text('An error occurred: ' + error.statusText);
            }
        });
    });

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
