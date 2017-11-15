# Copyright 2015-2016 Yelp Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import mock

from paasta_tools.cli.cmds.pause_autoscaler import MAX_PAUSE_DURATION
from paasta_tools.cli.cmds.pause_autoscaler import paasta_pause_autoscaler


def test_pause_autoscaler_defaults():
    args = mock.Mock(
        cluster='cluster1',
        duration='30',
        resume=False,
        info=False,
    )

    with mock.patch(
        'paasta_tools.cli.cmds.pause_autoscaler.update_autoscale_pause_time',
        autospec=True,
    ) as mock_exc:
        mock_exc.return_value = 0
        return_code = paasta_pause_autoscaler(args)
        mock_exc.assert_called_once_with('cluster1', '30')
        assert return_code == 0


def test_pause_autoscaler_long():
    args = mock.Mock(
        cluster='cluster1',
        duration=MAX_PAUSE_DURATION + 10,
        force=False,
        resume=False,
        info=False,
    )

    with mock.patch(
        'paasta_tools.cli.cmds.pause_autoscaler.update_autoscale_pause_time',
        autospec=True,
    ):
        return_code = paasta_pause_autoscaler(args)
        assert return_code == 3


def test_pause_autoscaler_resume():
    args = mock.Mock(
        cluster='cluster1',
        duration=120,
        force=False,
        resume=True,
        info=False,
    )

    with mock.patch(
        'paasta_tools.cli.cmds.pause_autoscaler.update_autoscale_pause_time',
        autospec=True,
    ) as mock_exc:
        return_code = paasta_pause_autoscaler(args)
        mock_exc.assert_called_once_with('cluster1', '0')
        assert return_code == 0


def test_pause_autoscaler_force():
    args = mock.Mock(
        cluster='cluster1',
        duration=str(MAX_PAUSE_DURATION + 10),
        force=True,
        resume=False,
        info=False,
    )

    with mock.patch(
        'paasta_tools.cli.cmds.pause_autoscaler.update_autoscale_pause_time',
        autospec=True,
    ) as mock_exc:
        return_code = paasta_pause_autoscaler(args)
        assert return_code == 0
        mock_exc.assert_called_once_with('cluster1', '330')


def test_pause_autoscaler_info():
    args = mock.Mock(
        cluster='cluster1',
        duration='30',
        force=False,
        resume=False,
        info=True,
    )

    with mock.patch(
        'paasta_tools.cli.cmds.pause_autoscaler.get_autoscale_pause_time',
        autospec=True,
    ) as mock_exc, mock.patch(
        'paasta_tools.cli.cmds.pause_autoscaler.time',
        autospec=True,
    ) as mock_time, mock.patch(
        'paasta_tools.cli.cmds.pause_autoscaler.paasta_print',
        autospec=True,
    ) as mock_print:
        mock_exc.return_value = 3
        mock_time.time.return_value = 6
        return_code = paasta_pause_autoscaler(args)
        mock_exc.assert_called_once_with('cluster1')
        mock_print.assert_called_once_with('Autoscaler is not paused')
        assert return_code == 0

        mock_exc.return_value = 3
        mock_time.time.return_value = 0
        return_code = paasta_pause_autoscaler(args)
        mock_print.assert_called_with('Autoscaler is paused until 00:00:03 1970-01-01')
        assert return_code == 0
