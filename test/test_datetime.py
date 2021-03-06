# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import unittest
import datetime

import arrow
import orjson
import pendulum
import pytz
from dateutil import tz


class DatetimeTests(unittest.TestCase):

    def test_datetime_naive(self):
        """
        datetime.datetime naive TypeError
        """
        with self.assertRaises(TypeError):
            orjson.dumps([datetime.datetime(2000, 1, 1, 2, 3, 4, 123)])

    def test_datetime_timezone_utc(self):
        """
        datetime.datetime UTC
        """
        self.assertEqual(
            orjson.dumps([datetime.datetime(2018, 6, 1, 2, 3, 4, 0, tzinfo=datetime.timezone.utc)]),
            b'["2018-06-01T02:03:04+00:00"]',
        )

    def test_datetime_pytz_utc(self):
        """
        datetime.datetime UTC
        """
        self.assertEqual(
            orjson.dumps([datetime.datetime(2018, 6, 1, 2, 3, 4, 0, tzinfo=pytz.UTC)]),
            b'["2018-06-01T02:03:04+00:00"]',
        )

    def test_datetime_pendulum_utc(self):
        """
        datetime.datetime UTC
        """
        self.assertEqual(
            orjson.dumps([datetime.datetime(2018, 6, 1, 2, 3, 4, 0, tzinfo=pendulum.UTC)]),
            b'["2018-06-01T02:03:04+00:00"]',
        )

    def test_datetime_arrow_positive(self):
        """
        datetime.datetime positive UTC
        """
        self.assertEqual(
            orjson.dumps([datetime.datetime(2018, 1, 1, 2, 3, 4, 0, tzinfo=tz.gettz('Asia/Shanghai'))]),
            b'["2018-01-01T02:03:04+08:00"]',
        )

    def test_datetime_pytz_positive(self):
        """
        datetime.datetime positive UTC
        """
        self.assertEqual(
            orjson.dumps([datetime.datetime(2018, 1, 1, 2, 3, 4, 0, tzinfo=pytz.timezone('Asia/Shanghai'))]),
            b'["2018-01-01T02:03:04+08:00"]',
        )

    def test_datetime_pendulum_positive(self):
        """
        datetime.datetime positive UTC
        """
        self.assertEqual(
            orjson.dumps([datetime.datetime(2018, 1, 1, 2, 3, 4, 0, tzinfo=pendulum.timezone('Asia/Shanghai'))]),
            b'["2018-01-01T02:03:04+08:00"]',
        )

    def test_datetime_pytz_negative_dst(self):
        """
        datetime.datetime negative UTC DST
        """
        self.assertEqual(
            orjson.dumps([datetime.datetime(2018, 6, 1, 2, 3, 4, 0, tzinfo=pytz.timezone('America/New_York'))]),
            b'["2018-06-01T02:03:04-04:00"]',
        )

    def test_datetime_pendulum_negative_dst(self):
        """
        datetime.datetime negative UTC DST
        """
        self.assertEqual(
            orjson.dumps([datetime.datetime(2018, 6, 1, 2, 3, 4, 0, tzinfo=pendulum.timezone('America/New_York'))]),
            b'["2018-06-01T02:03:04-04:00"]',
        )

    def test_datetime_pytz_negative_non_dst(self):
        """
        datetime.datetime negative UTC non-DST
        """
        self.assertEqual(
            orjson.dumps([datetime.datetime(2018, 12, 1, 2, 3, 4, 0, tzinfo=pytz.timezone('America/New_York'))]),
            b'["2018-12-01T02:03:04-05:00"]',
        )

    def test_datetime_pendulum_negative_non_dst(self):
        """
        datetime.datetime negative UTC non-DST
        """
        self.assertEqual(
            orjson.dumps([datetime.datetime(2018, 12, 1, 2, 3, 4, 0, tzinfo=pendulum.timezone('America/New_York'))]),
            b'["2018-12-01T02:03:04-05:00"]',
        )

    def test_datetime_partial_hour(self):
        """
        datetime.datetime UTC offset partial hour
        """
        self.assertEqual(
            orjson.dumps([datetime.datetime(2018, 12, 1, 2, 3, 4, 0, tzinfo=pytz.timezone('Australia/Adelaide'))]),
            b'["2018-12-01T02:03:04+10:30"]',
        )

    def test_datetime_pytz_partial_hour(self):
        """
        datetime.datetime UTC offset partial hour
        """
        self.assertEqual(
            orjson.dumps([datetime.datetime(2018, 12, 1, 2, 3, 4, 0, tzinfo=pytz.timezone('Australia/Adelaide'))]),
            b'["2018-12-01T02:03:04+10:30"]',
        )

    def test_datetime_pendulum_partial_hour(self):
        """
        datetime.datetime UTC offset partial hour
        """
        self.assertEqual(
            orjson.dumps([datetime.datetime(2018, 12, 1, 2, 3, 4, 0, tzinfo=pendulum.timezone('Australia/Adelaide'))]),
            b'["2018-12-01T02:03:04+10:30"]',
        )

    def test_datetime_partial_second(self):
        """
        datetime.datetime UTC offset round seconds

        https://tools.ietf.org/html/rfc3339#section-5.8
        """
        self.assertEqual(
            orjson.dumps([datetime.datetime(1937, 1, 1, 12, 0, 27, 87, tzinfo=pendulum.timezone('Europe/Amsterdam'))]),
            b'["1937-01-01T12:00:27.87+00:20"]',
        )


class DateTests(unittest.TestCase):

    def test_date(self):
        """
        datetime.date
        """
        self.assertEqual(
            orjson.dumps([datetime.date(2000, 1, 13)]),
            b'["2000-01-13"]',
        )

    def test_date_min(self):
        """
        datetime.date MINYEAR
        """
        self.assertEqual(
            orjson.dumps([datetime.date(datetime.MINYEAR, 1, 1)]),
            b'["1-01-01"]',
        )

    def test_date_max(self):
        """
        datetime.date MAXYEAR
        """
        self.assertEqual(
            orjson.dumps([datetime.date(datetime.MAXYEAR, 12, 31)]),
            b'["9999-12-31"]',
        )


class TimeTests(unittest.TestCase):

    def test_time(self):
        """
        datetime.time
        """
        self.assertEqual(
            orjson.dumps([datetime.time(12, 15, 59, 111)]),
            b'["12:15:59.111"]',
        )
        self.assertEqual(
            orjson.dumps([datetime.time(12, 15, 59)]),
            b'["12:15:59"]',
        )

    def test_time_tz(self):
        """
        datetime.time with tzinfo error
        """
        with self.assertRaises(orjson.JSONEncodeError):
            orjson.dumps([datetime.time(12, 15, 59, 111, tzinfo=tz.gettz('Asia/Shanghai'))]),
