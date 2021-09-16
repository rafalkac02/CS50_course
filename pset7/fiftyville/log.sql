-- Keep a log of any SQL queries you execute as you solve the mystery.

-- 1. Find the description of the crime
SELECT street, description FROM crime_scene_reports
WHERE street LIKE '%Chamberlin%' AND year = '2020' AND month = '7' AND day = '28';

-- Output:
-- "Chamberlin Street | Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
-- Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse."

-- 2. Thus, let's find testimonies of wintnesses
SELECT name, transcript FROM interviews
WHERE transcript LIKE '%courthouse%' AND year = 2020 AND month = 7;

-- Output:
-- Ruth | Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away. If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
-- Eugene | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
-- Raymond | As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- According to testimonies, the thief:
    -- was leaving by car shortly after crime,
    -- was withdrawing money earlier that day,
    -- called an accomplice as he was leaving the courthouse, revealing plan to take earliest flight the next day. The accomplice was supposed to buy the tickets.


-- 3. Let's then find people who on July 28, 2020 were:
    -- withdrawing money before 10:15am
    -- making a call and talk less than a minute shortly after 10:15am,
    -- leaving courThouse within 10 minutes after 10:15am
    -- having the earliest flight next day

WITH withdraws AS
(
    SELECT name FROM people
    JOIN bank_accounts ON people.id = bank_accounts.person_id
    JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
    WHERE year = 2020 AND month = 7 AND day = 28 AND transaction_type = 'withdraw'
),

calls AS
(
    SELECT name FROM people
    JOIN phone_calls ON people.phone_number = phone_calls.caller
    WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60
),

security AS
(
    SELECT name FROM people
    JOIN courthouse_security_logs ON people.license_plate = courthouse_security_logs.license_plate
    WHERE activity = 'exit' AND year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25
),

flight AS
(
    SELECT name FROM people
    JOIN passengers ON people.passport_number = passengers.passport_number
    WHERE flight_id IN
        (
            SELECT id FROM flights
            WHERE year = 2020 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1
        )
)

SELECT name FROM people WHERE name IN withdraws AND name IN calls AND name IN security AND name IN flight;

-- Query outputs the name of the tief: Ernest


-- 4. let's look for the thief's accomplice - the one who received a call from Ernest

SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60
AND caller IN (SELECT phone_number FROM people WHERE name = 'Ernest');

-- Accomplice is Berthold

-- 5. Lastly, let's where the thief escaped to

SELECT city FROM airports
JOIN flights ON airports.id = flights.destination_airport_id
WHERE year = 2020 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1;

-- The thief escaped to London