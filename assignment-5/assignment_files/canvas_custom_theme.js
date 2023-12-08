/*
 * 2019-02-12 Therese Eriksson, Therese Webbutveckling AB
 * Remove column sis id from users table when users are loaded
 * 
 * 2019-11-07 Rolf Johansson, Chalmers
 * Since SIS ID can appear in different :nth-child TD, search for it first.
 * Also handle dynamic loading and filtering.
 * 
 * 2020-02-06 Rolf Johansson, Chalmers
 * Add function to filter out certain strings, in production "@chalmers.se"
 * table cells (for Login ID).
 * 
 * 2022-03-09 Rolf Johansson, Chalmers
 * Added mutation observer to replace placeholder text in textarea for adding users,
 * since the attribute is changed dynamically depending on radio button click.
 */

(function() {
    'use strict';
    let c_selfSignupUserData = {};
    var totalColumns = -1,
        removedColumn = -1;
    var contentNode = document.getElementById('content'),
        addMutationObserver = function(node, config, callback) {
            var observer = new MutationObserver(callback);
            observer.observe(node, config);
        },
        removeTableColumn = function(mutationList, contentNode, searchString) {
            var addedNodes = [];
            mutationList.forEach(m => m.addedNodes.forEach(n => addedNodes.push(n)));
            if (addedNodes.length > 0) {
                var column = removedColumn > 0 ? removedColumn : -1;
                var colHead = contentNode.querySelectorAll('table tr th');
                if (totalColumns < 0 && colHead.length > 0) {
                    totalColumns = colHead.length;
                }
                if (colHead.length > 0) {
                    if (column < 0) {
                        for (var i = 0; i < colHead.length; i++) {
                            if (colHead[i].innerHTML.startsWith(searchString)) {
                                column = i + 1;
                            }
                        }
                    }
                    if (column > 0) {
                        if (colHead.length == totalColumns) {
                            var nodeTh = contentNode.querySelectorAll('table tr th:nth-child(' + column + ')')[0];
                            nodeTh.parentNode.removeChild(nodeTh);
                            removedColumn = column;
                        }
                        var rosterTable = contentNode.querySelectorAll('table.roster')[0];
                        var userRows = rosterTable.querySelectorAll('.rosterUser');
                        Array.prototype.forEach.call(userRows, function(userRow) {
                            if (userRow.querySelectorAll('td').length == totalColumns) {
                                var nodeTd = userRow.querySelectorAll('td:nth-child(' + column + ')')[0];
                                nodeTd.parentNode.removeChild(nodeTd);
                            }
                        });
                    }
                }
            } else {}
        },
        changeStringInTableCells = function(mutationList, contentNode, searchString, replaceString) {
            var addedNodes = [];
            mutationList.forEach(m => m.addedNodes.forEach(n => addedNodes.push(n)));
            if (addedNodes.length > 0) {
                let cells = contentNode.querySelectorAll('table tr td');
                if (cells.length > 0) {
                    for (var i = 0; i < cells.length; i++) {
                        if (cells[i].innerText.includes(searchString)) {
                            cells[i].innerText = cells[i].innerText.replace(searchString, replaceString);
                        }
                    }
                }
            }
        },
        replaceTextareaPlaceholder = function(mutations, search, replace) {
            mutations.forEach(function(mutation) {
                if (mutation.type == "attributes" && mutation.attributeName == "placeholder" && mutation.target.placeholder == search) {
                    document.getElementById(mutation.target.id).setAttribute("placeholder", replace);
                }
            });
        };

    // Location /courses/13/users
    if (window.location.pathname.match(/\/courses\/([0-9]+)\/users((\/$)|$)/gm)) {
        addMutationObserver(
            contentNode, {
                childList: true,
                subtree: true
            },
            function(mutationList) {
                removeTableColumn(mutationList, contentNode, "SIS ID");
                changeStringInTableCells(mutationList, contentNode, "@chalmers.se", "");
            }
        );
    }
    // Location /courses/13/users and /account/1
    // Add people dialog is loaded as extra div on button click, we need to observe whole body to catch it loading
    if (window.location.pathname.match(/\/courses\/([0-9]+)\/users((\/$)|$)/gm) || window.location.pathname.match(/\/accounts\/([0-9]+)(\?$|$)/gm)) {
        addMutationObserver(
            document.body, {
                childList: true,
                attributes: true,
                subtree: true
            },
            function(mutationList) {
                replaceTextareaPlaceholder(mutationList, "lsmith, mfoster", "CID@chalmers.se or GUS");
            }
        );
    }
    // Test self signup limiter
    if (window.location.pathname.match(/\/courses\/29889\/groups((\/$)|$)/gm)) {
        console.log("_css: start");
        fetch(`https://canvas-cth-lti-group-tool-development.azurewebsites.net/api/self-signup/${ENV.course_id}/${ENV.current_user.id}`).then(response => response.json()).then(data => {
            console.log("_css: first fetch");
            console.log(data);
            c_selfSignupUserData = data;
        }).then(finished => {
            console.log("_css: first fetch finish, adding mutation observer on contentNode");
            addMutationObserver(
                contentNode, 
                {
                    childList: true,
                    attributes: true,
                    subtree: true
                },
                function (mutationList) {
                    console.log("_css: mutation observed");
                    mutationList.forEach(function (mutation) {
                        if (mutation.type == "childList" && mutation.addedNodes) {
                            mutation.addedNodes.forEach(function (node) {
                                if (node.nodeName == "DIV" && node.querySelector("div.student-group-body")) {
                                    let group_id = parseInt(node.querySelector("div.student-group-body")?.getAttribute("id").replace("student-group-body-", ""));
                                    console.log("_css: Group id (in if, integer): " + group_id);
                                    if (Object.keys(c_selfSignupUserData).length) {
                                        if (group_id != null && c_selfSignupUserData.groups.map(x => x.id).includes(group_id)) {
                                            console.log(c_selfSignupUserData.groups.find(x => x.id === group_id));
                                            if (!c_selfSignupUserData.groups.find(x => x.id === group_id).passed) {
                                                node.querySelector("span.student-group-join button").style.display = "none";
                                                let d = document.createElement("div");
                                                d.innerText = c_selfSignupUserData.groups.find(x => x.id === group_id).description;
                                                d.classList.add("c-self-signup-locked-text");
                                                node.querySelector("div.student-group-title").appendChild(d);
                                                console.log("_css: Hiding join button, not passed for group id " + group_id);
                                            }
                                            else {
                                                console.log("_css: Nothing to do.");
                                            }
                                        }
                                        else if (group_id != null && c_selfSignupUserData.groups.length == 0 && c_selfSignupUserData.success) {
                                            console.log("_css: No group data in public api result, but ok. Do nothing.");
                                        }
                                    }
                                    else {
                                        console.log("_css: No data at all from public api, this should not happen. Lock all groups?");
                                    }
                                }
                            });
                        }
                    });
                }
            );
        });
    }
})();