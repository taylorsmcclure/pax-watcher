# pax-watcher
Python based program to watch the PAX Prime ticket page for changes and then trigger an SNS alarm.

<h2>How it works</h2>
<ol>
<li>The AWS Lambda function is uploaded with required modules.</li>
<li>CloudWatch Events invokes the Lambda function every x minutes</li>
<li>Lambda function grabs HTML ID 'badgeAvailability' on the PAX site http://prime.paxsite.com/registration</li>
<li>The function compares this result to the expected result from S3, if the result is different, it invokes a SNS topic</li>
</ol>
