
/*
 * 2019-02-12 Therese Eriksson, Therese Webbutveckling AB
 * Remove column sis id from users table when users are loaded
 */

(function () {
    'use strict';

    var contentNode = document.getElementById('content'),
        addMutationObserver = function (node, config, callback) {
            // Create an observer instance linked to the callback function
            var observer = new MutationObserver(callback);

            // Start observing the target node for configured mutations
            observer.observe(node, config);
        },
        removeSisIdHead = function (contentNode) {
            var colHead = contentNode.querySelectorAll('table tr th:nth-child(4)')[0];

            if (colHead === undefined) {
                // Table hasn't loaded yet
                return;
            }
            if (colHead.innerHTML !== 'SIS ID') {
                // SIS ID is already removed
                return;
            }
            var removeCols = contentNode.querySelectorAll('table tr th:nth-child(4)');

            Array.prototype.forEach.call(removeCols, function (node) {
                node.parentNode.removeChild(node);
            });
        },
        removeSisIdInUserRows = function (contentNode) {
            var rosterTable = contentNode.querySelectorAll('table.roster')[0];

            if (rosterTable === undefined) {
                // Table hasn't loaded yet
                return;
            }
            var userRows = rosterTable.querySelectorAll('.rosterUser');

            Array.prototype.forEach.call(userRows, function (userRow) {
                if (userRow.querySelectorAll('td').length === 9) {
                    var node = userRow.querySelectorAll('td:nth-child(4)')[0];
                    node.parentNode.removeChild(node);
                }
            });
        };

    // Location /courses/13/users
    if (window.location.pathname.match(/\/courses\/([0-9]+)\/users((\/$)|$)/gm)) {
        addMutationObserver(
            contentNode,
            {
                childList: true,
                subtree: true
            },
            function () {
                removeSisIdHead(contentNode);
                removeSisIdInUserRows(contentNode);
            }
        );
    }
})();

