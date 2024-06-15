$(document).ready(function () {
    const $sidebar = $('#sidebar');
    const $toggleButton = $('#toggleButton');
    const $runScriptNav = $('#runScriptNav');
    const $viewInfoNav = $('#viewInfoNav');
    const $createCronNav = $('#createCronNav');
    const $runScriptContainer = $('#runScriptContainer');
    const $createCronContainer = $('#createCronContainer');
    const $viewInfoContainer = $('#viewInfoContainer');
    const $content = $('#content');
    const $output = $('#output');
    const $infoOutput = $('#infoOutput');
    const $cronOutput = $('#cronOutput');

    // Toggle sidebar
    $toggleButton.on('click', function () {
        $sidebar.toggleClass('open');
        if ($sidebar.hasClass('open')) {
            $toggleButton.css('left', '250px');
            $content.css('marginLeft', '250px');
        } else {
            $toggleButton.css('left', '0');
            $content.css('marginLeft', '0');
        }
    });

    // Navigation click handlers
    const navClickHandler = function ($activeContainer) {
        $runScriptContainer.removeClass('active');
        $createCronContainer.removeClass('active');
        $viewInfoContainer.removeClass('active');
        $activeContainer.addClass('active');
    };

    $runScriptNav.on('click', () => navClickHandler($runScriptContainer));
    $viewInfoNav.on('click', () => navClickHandler($viewInfoContainer));
    $createCronNav.on('click', () => navClickHandler($createCronContainer));

    // Run script
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

    // Populate table
    function populateTable(data, isDevice) {
        const $thead = $infoOutput.find('thead tr');
        const $tbody = $infoOutput.find('tbody');
        $tbody.empty();
        $thead.empty();

        if (data.error) {
            $tbody.append(`<tr><td colspan="3">Error: ${data.error}</td></tr>`);
        } else {
            const headers = isDevice ? '<th>Device ID</th>' : '<th>Last Name</th><th>Name</th><th>User ID</th>';
            $thead.append(headers);

            data.forEach(item => {
                const row = isDevice ? `<tr><td>${item.device_id}</td></tr>` : `<tr><td>${item.last_name}</td><td>${item.name}</td><td>${item.user_id}</td></tr>`;
                $tbody.append(row);
            });
        }
    }

    // Fetch device info
    $('#getDeviceInfoButton').on('click', function () {
        $.ajax({
            url: '/api/devices',
            method: 'GET',
            success: function (data) {
                populateTable(data, true);
            },
            error: function (error) {
                $infoOutput.find('tbody').html(`<tr><td colspan="3">An error occurred: ${error.statusText}</td></tr>`);
            }
        });
    });

    // Fetch user info
    $('#getUserInfoButton').on('click', function () {
        $.ajax({
            url: '/api/users',
            method: 'GET',
            success: function (data) {
                populateTable(data, false);
            },
            error: function (error) {
                $infoOutput.find('tbody').html(`<tr><td colspan="3">An error occurred: ${error.statusText}</td></tr>`);
            }
        });
    });

    // Create cron job
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

    // Set default active section
    $runScriptContainer.addClass('active');
});
