$(document).ready(function () {


    function populateTable(data, isDevice, tableId) {
        const $infoOutput = $(tableId);
        const $thead = $infoOutput.find('thead tr');
        const $tbody = $infoOutput.find('tbody');
        $tbody.empty();
        $thead.empty();

        if (data.error) {
            $tbody.append(`<tr><td colspan="3">Error: ${data.error}</td></tr>`);
        } else {
            const headers = isDevice ? '<th>Device ID</th>' : '<th>Username</th><th>Phone Number</th><th>Email</th>';
            $thead.append(headers);

            data.forEach(item => {
                const row = isDevice ? `<tr><td>${item.device_id}</td></tr>` : `<tr><td>${item.name} ${item.last_name}</td><td>${item.phone_number}</td><td>${item.email}</td></tr>`;
                $tbody.append(row);
            });
        }
    }

    $.ajax({
        url: '/api/devices',
        method: 'GET',
        success: function (data) {
            populateTable(data, true, '#infoOutput');
        },
        error: function (error) {
            $infoOutput.find('tbody').html(`<tr><td colspan="3">An error occurred: ${error.statusText}</td></tr>`);
        }
    });
    $.ajax({
        url: '/api/users',
        method: 'GET',
        success: function (data) {
            populateTable(data, false, userInfoOutput);
        },
        error: function (error) {
            $infoOutput.find('tbody').html(`<tr><td colspan="3">An error occurred: ${error.statusText}</td></tr>`);
        }
    });
});
