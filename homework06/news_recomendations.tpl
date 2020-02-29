﻿<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
	<centre><b>Score: {{score}}</b></centre>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead>
                <th>Title</th>
                <th>Predict Label</th>
            </thead>
            <tbody>
                %for row in rows:
                <tr>
                    <td>{{ row['title'] }}</td>
                    <td>{{ row['label'] }}</td>
                </tr>
                %end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/news" class="button">Go Back</a>
                    </th>
                </tr>
            </tfoot>
        </table>
        </div>
    </body>
</html>