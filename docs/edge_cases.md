# Edge Cases considered for the Cron Expression Parser Service

Cron Expressions present a lot of interesting problems to account for and consider. This document covers edge cases that we should consider in future such as date validation, cyclic or backward ranges and leap years.

### Date and Month validation

This service should ensure that the days and month provided make sense. For example, February 30 doesn't exist, so if a user provides "30 2" for Day of Month and Month fields, we should return an error gracefully.

I could introduce a simple CronValidator to handle this, and we can use this validator to handle/account for other potential edge cases.

### Cyclic / Backward Ranges

Cron Expressions can contain ranges such as 1-5 for days of the week. We should dtermine how we handle these in the system. For example, 5-2 may imply Friday (5) to Tuesday (2).

In this initial implementation, I will class cyclic / backward ranges as invalid, however, we can always implement support for cyclic ranges if our customers require it. 

```
cron_string = "0 12 5-2 * * /path/to/task.sh" 
```

This should raise an error because the range is backward. If cyclic ranges are allowed, interpret as Friday to Tuesday.



### Invalid strings

A cron string must contain exactly 5 parts, followed by a command. We handle this in our code by raising a InvalidCronFormatError when this fails.