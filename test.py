from datetime import datetime

import numpy as np
import pandas as pd
from opcua import Client
from opcua.ua import DataValue, Variant, VariantType

from messages_pb2 import NumpyArray

def main_realtime():
    ua_client = Client("opc.tcp://10.41.192.191:4840")
    ua_client.session_timeout = 120000
    ua_client.set_user("admin")
    ua_client.set_password("DeltaRobot2020")

    ua_client.connect()
    j = 0
    while True:
        if ua_client:
            ready_for_trigger_node = ua_client.get_node('ns=3;s="LEdgeBuffer_SwitchBuffer"."readyForTrigger"')
            enable_switch_buffer_node = ua_client.get_node('ns=3;s="LEdgeBuffer_SwitchBuffer"."enableSwitchBuffer"')
            start_recording_node = ua_client.get_node('ns=3;s="LEdgeBuffer_SwitchBuffer"."startRecording"')
            currentBufferStateMachine_Node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."currentBufferStateMachine"')

            # Read number of traces
            lrealTraceSelectorParent = ua_client.get_node('ns=3;s="LEdgeBuffer_SwitchBuffer"."lrealTraceSelector"')
            val = lrealTraceSelectorParent.get_data_value()
            val = val.Value.Value
            num_of_traces = len(val)
            print(f'Number of traces: {num_of_traces}')

            lreal_signal_used_nodes = [ua_client.get_node(f'ns=3;s="LEdgeBuffer_SwitchBuffer"."lrealSignalUsed"[{i}]')
                                       for i in range(0, num_of_traces)]

            lreal_trace_selector_nodes = [
                ua_client.get_node(f'ns=3;s="LEdgeBuffer_SwitchBuffer"."lrealTraceSelector"[{i}]') for i in
                range(0, num_of_traces)]

            trace_names_nodes = [
                ua_client.get_node(f'ns=3;s="LEdgeBuffer_SwitchBuffer"."signals"."lreals"."traceSignal"[{i}]."name"')
                for i in range(0, num_of_traces)]

            # Define nodes for edgeInterface0 (handshakeBit, samples, timeStamps)
            eI0handsake_bit_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."handshakeBit"')
            eI0sample_nodes = [ua_client.get_node(
                f'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."samples"."signalLREAL"[{i}]."sampleNo"')
                for i in range(0, num_of_traces)]
            eI0time_stamp_first_sample_year_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSampleTimestamp"[0]')
            eI0time_stamp_first_sample_month_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSampleTimestamp"[1]')
            eI0time_stamp_first_sample_day_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSampleTimestamp"[2]')
            eI0time_stamp_first_sample_hours_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSampleTimestamp"[3]')
            eI0time_stamp_first_sample_minutes_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSampleTimestamp"[4]')
            eI0time_stamp_first_sample_seconds_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSampleTimestamp"[5]')
            eI0time_stamp_first_sample_ns_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSampleTimestamp"[6]')
            eI0time_stamp_last_sample_year_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."lastSampleTimestamp"[0]')
            eI0time_stamp_last_sample_month_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."lastSampleTimestamp"[1]')
            eI0time_stamp_last_sample_day_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."lastSampleTimestamp"[2]')
            eI0time_stamp_last_sample_hours_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."lastSampleTimestamp"[3]')
            eI0time_stamp_last_sample_minutes_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."lastSampleTimestamp"[4]')
            eI0time_stamp_last_sample_seconds_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."lastSampleTimestamp"[5]')
            eI0time_stamp_last_sample_ns_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."lastSampleTimestamp"[6]')
            eI0first_sample_after_pretrigger_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSample"')

            # Define nodes for edgeInterface1 (handshakeBit, samples, timeStamps)
            eI1handsake_bit_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."handshakeBit"')
            # 1,2,3,4,5,6,7,8,9,10
            eI1sample_nodes = [ua_client.get_node(
                f'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."samples"."signalLREAL"[{i}]."sampleNo"')
                for i in range(0, num_of_traces)]
            eI1time_stamp_first_sample_year_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."firstTriggerSampleTimestamp"[0]')
            eI1time_stamp_first_sample_month_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."firstTriggerSampleTimestamp"[1]')
            eI1time_stamp_first_sample_day_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."firstTriggerSampleTimestamp"[2]')
            eI1time_stamp_first_sample_hours_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."firstTriggerSampleTimestamp"[3]')
            eI1time_stamp_first_sample_minutes_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."firstTriggerSampleTimestamp"[4]')
            eI1time_stamp_first_sample_seconds_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."firstTriggerSampleTimestamp"[5]')
            eI1time_stamp_first_sample_ns_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."firstTriggerSampleTimestamp"[6]')
            eI1time_stamp_last_sample_year_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."lastSampleTimestamp"[0]')
            eI1time_stamp_last_sample_month_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."lastSampleTimestamp"[1]')
            eI1time_stamp_last_sample_day_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."lastSampleTimestamp"[2]')
            eI1time_stamp_last_sample_hours_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."lastSampleTimestamp"[3]')
            eI1time_stamp_last_sample_minutes_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."lastSampleTimestamp"[4]')
            eI1time_stamp_last_sample_seconds_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."lastSampleTimestamp"[5]')
            eI1time_stamp_last_sample_ns_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."lastSampleTimestamp"[6]')

            traj_contains_flag_node = ua_client.get_node('ns=3;s="Buffer_data"."Data"."TrajectoryContainsFlags"')

            num_of_packets = 24

            # Data transfer
            # Step 0
            enable_switch_buffer_node.set_value(DataValue(Variant(False, VariantType.Boolean)))

            # Step 1
            signal_used_cell = [1] * num_of_traces
            for node, value in zip(lreal_signal_used_nodes, signal_used_cell):
                node.set_value(DataValue(Variant(value, VariantType.Boolean)))

            trace_selector_cell = [i for i in range(num_of_traces)]

            for node, value in zip(lreal_trace_selector_nodes, trace_selector_cell):
                node.set_value(DataValue(Variant(value, VariantType.Int16)))

            # Step 1.5
            val = eI0sample_nodes[0].get_data_value()
            val = val.Value.Value
            size_of_packet = len(val)
            samples = np.zeros((num_of_traces, size_of_packet * num_of_packets))
            time_first_and_last_matrix = np.zeros((14, num_of_packets))
            print(f"Size of packets: {size_of_packet}")

            # Step 2
            enable_switch_buffer_node.set_value(DataValue(Variant(True, VariantType.Boolean)))

            # Step 3
            val = [node.get_data_value() for node in trace_names_nodes]
            trace_names = [str(v.Value.Value) for v in val]
            rft = 0
            while rft == 0:
                ready_for_trigger = ready_for_trigger_node.get_data_value().Value.Value
                rft = ready_for_trigger

            # Step 3.5
            print("Waiting on flag")
            traj_contains_flag = 0
            while traj_contains_flag == 0:
                traj_contains_flag_read = traj_contains_flag_node.get_data_value().Value.Value
                traj_contains_flag = traj_contains_flag_read

            # Step 4
            start_recording_node.set_value(DataValue(Variant(True, VariantType.Boolean)))
            print("step 4")

            # Step 5 - loop to read samples in packages
            print("step 5")

            packet_no = 0
            while packet_no < num_of_packets:

                if packet_no % 2 == 0:  # edgeInterface[0]
                    hs_bit0 = 0
                    while hs_bit0 == 0:
                        # print("waiting for handshake bit if0")
                        hs_bit0_read = eI0handsake_bit_node.get_data_value().Value.Value
                        hs_bit0 = hs_bit0_read

                    val = [node.get_data_value() for node in eI0sample_nodes]

                    arr_to_stream = [val[i].Value.Value for i in range(4, 11)]
                    arr_to_stream = np.array(arr_to_stream)
                    yield arr_to_stream

                    eI0handsake_bit_node.set_value(DataValue(Variant(False, VariantType.Boolean)))

                    for i in range(num_of_traces):
                        samples[i, packet_no * size_of_packet:(packet_no + 1) * size_of_packet] = val[i].Value.Value


                    val = [node.get_data_value() for node in
                           [eI0time_stamp_first_sample_year_node, eI0time_stamp_first_sample_month_node,
                            eI0time_stamp_first_sample_day_node, eI0time_stamp_first_sample_hours_node,
                            eI0time_stamp_first_sample_minutes_node, eI0time_stamp_first_sample_seconds_node,
                            eI0time_stamp_first_sample_ns_node, eI0time_stamp_last_sample_year_node,
                            eI0time_stamp_last_sample_month_node, eI0time_stamp_last_sample_day_node,
                            eI0time_stamp_last_sample_hours_node, eI0time_stamp_last_sample_minutes_node,
                            eI0time_stamp_last_sample_seconds_node, eI0time_stamp_last_sample_ns_node]]
                    for i in range(14):
                        time_first_and_last_matrix[i, packet_no] = val[i].Value.Value

                    if packet_no == 0:
                        first_sample_after_pretrigger_read = eI0first_sample_after_pretrigger_node.get_data_value().Value.Value
                        first_sample_after_pretrigger = float(first_sample_after_pretrigger_read)

                elif packet_no % 2 == 1:  # edgeInterface[1]
                    hs_bit1 = 0
                    while hs_bit1 == 0:
                        # print("waiting for handshake bit if1")
                        hs_bit1_read = eI1handsake_bit_node.get_data_value().Value.Value
                        hs_bit1 = hs_bit1_read
                    val = [node.get_data_value() for node in eI1sample_nodes]

                    arr_to_stream = [val[i].Value.Value for i in range(4, 11)]
                    arr_to_stream = np.array(arr_to_stream)
                    yield arr_to_stream

                    eI1handsake_bit_node.set_value(DataValue(Variant(False, VariantType.Boolean)))

                    for i in range(num_of_traces):
                        samples[i, packet_no * size_of_packet:(packet_no + 1) * size_of_packet] = val[i].Value.Value

                    val = [node.get_data_value() for node in
                           [eI1time_stamp_first_sample_year_node, eI1time_stamp_first_sample_month_node,
                            eI1time_stamp_first_sample_day_node, eI1time_stamp_first_sample_hours_node,
                            eI1time_stamp_first_sample_minutes_node, eI1time_stamp_first_sample_seconds_node,
                            eI1time_stamp_first_sample_ns_node, eI1time_stamp_last_sample_year_node,
                            eI1time_stamp_last_sample_month_node, eI1time_stamp_last_sample_day_node,
                            eI1time_stamp_last_sample_hours_node, eI1time_stamp_last_sample_minutes_node,
                            eI1time_stamp_last_sample_seconds_node, eI1time_stamp_last_sample_ns_node]]
                    for i in range(14):
                        time_first_and_last_matrix[i, packet_no] = val[i].Value.Value

                else:
                    raise ValueError('Invalid index of edgeInterface')

                packet_no += 1

            enable_switch_buffer_node.set_value(DataValue(Variant(False, VariantType.Boolean)))
            # ua_client.disconnect()
            init_server = 0
            print('Transfer done. Postprocessing the data...')

            current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            np.save(f"samples{j}_{str(current_datetime)}.npy", samples)

            j += 1
            # transposed_array = samples.T
            # selected_cols = transposed_array[:, 4:10]


            print('Done')


def main():
    ua_client = Client("opc.tcp://10.41.192.191:4840")
    ua_client.session_timeout = 120000
    ua_client.set_user("admin")
    ua_client.set_password("DeltaRobot2020")

    ua_client.connect()
    j = 0
    while True:
        if ua_client:
            ready_for_trigger_node = ua_client.get_node('ns=3;s="LEdgeBuffer_SwitchBuffer"."readyForTrigger"')
            enable_switch_buffer_node = ua_client.get_node('ns=3;s="LEdgeBuffer_SwitchBuffer"."enableSwitchBuffer"')
            start_recording_node = ua_client.get_node('ns=3;s="LEdgeBuffer_SwitchBuffer"."startRecording"')
            currentBufferStateMachine_Node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."currentBufferStateMachine"')

            # Read number of traces
            lrealTraceSelectorParent = ua_client.get_node('ns=3;s="LEdgeBuffer_SwitchBuffer"."lrealTraceSelector"')
            val = lrealTraceSelectorParent.get_data_value()
            val = val.Value.Value
            num_of_traces = len(val)
            print(f'Number of traces: {num_of_traces}')

            lreal_signal_used_nodes = [ua_client.get_node(f'ns=3;s="LEdgeBuffer_SwitchBuffer"."lrealSignalUsed"[{i}]')
                                       for i in range(0, num_of_traces)]

            lreal_trace_selector_nodes = [
                ua_client.get_node(f'ns=3;s="LEdgeBuffer_SwitchBuffer"."lrealTraceSelector"[{i}]') for i in
                range(0, num_of_traces)]

            trace_names_nodes = [
                ua_client.get_node(f'ns=3;s="LEdgeBuffer_SwitchBuffer"."signals"."lreals"."traceSignal"[{i}]."name"')
                for i in range(0, num_of_traces)]

            # Define nodes for edgeInterface0 (handshakeBit, samples, timeStamps)
            eI0handsake_bit_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."handshakeBit"')
            eI0sample_nodes = [ua_client.get_node(
                f'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."samples"."signalLREAL"[{i}]."sampleNo"')
                for i in range(0, num_of_traces)]
            eI0time_stamp_first_sample_year_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSampleTimestamp"[0]')
            eI0time_stamp_first_sample_month_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSampleTimestamp"[1]')
            eI0time_stamp_first_sample_day_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSampleTimestamp"[2]')
            eI0time_stamp_first_sample_hours_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSampleTimestamp"[3]')
            eI0time_stamp_first_sample_minutes_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSampleTimestamp"[4]')
            eI0time_stamp_first_sample_seconds_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSampleTimestamp"[5]')
            eI0time_stamp_first_sample_ns_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSampleTimestamp"[6]')
            eI0time_stamp_last_sample_year_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."lastSampleTimestamp"[0]')
            eI0time_stamp_last_sample_month_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."lastSampleTimestamp"[1]')
            eI0time_stamp_last_sample_day_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."lastSampleTimestamp"[2]')
            eI0time_stamp_last_sample_hours_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."lastSampleTimestamp"[3]')
            eI0time_stamp_last_sample_minutes_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."lastSampleTimestamp"[4]')
            eI0time_stamp_last_sample_seconds_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."lastSampleTimestamp"[5]')
            eI0time_stamp_last_sample_ns_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."lastSampleTimestamp"[6]')
            eI0first_sample_after_pretrigger_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[0]."dataBuffer"."header"."firstTriggerSample"')

            # Define nodes for edgeInterface1 (handshakeBit, samples, timeStamps)
            eI1handsake_bit_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."handshakeBit"')
            # 1,2,3,4,5,6,7,8,9,10
            eI1sample_nodes = [ua_client.get_node(
                f'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."samples"."signalLREAL"[{i}]."sampleNo"')
                for i in range(0, num_of_traces)]
            eI1time_stamp_first_sample_year_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."firstTriggerSampleTimestamp"[0]')
            eI1time_stamp_first_sample_month_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."firstTriggerSampleTimestamp"[1]')
            eI1time_stamp_first_sample_day_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."firstTriggerSampleTimestamp"[2]')
            eI1time_stamp_first_sample_hours_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."firstTriggerSampleTimestamp"[3]')
            eI1time_stamp_first_sample_minutes_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."firstTriggerSampleTimestamp"[4]')
            eI1time_stamp_first_sample_seconds_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."firstTriggerSampleTimestamp"[5]')
            eI1time_stamp_first_sample_ns_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."firstTriggerSampleTimestamp"[6]')
            eI1time_stamp_last_sample_year_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."lastSampleTimestamp"[0]')
            eI1time_stamp_last_sample_month_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."lastSampleTimestamp"[1]')
            eI1time_stamp_last_sample_day_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."lastSampleTimestamp"[2]')
            eI1time_stamp_last_sample_hours_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."lastSampleTimestamp"[3]')
            eI1time_stamp_last_sample_minutes_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."lastSampleTimestamp"[4]')
            eI1time_stamp_last_sample_seconds_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."lastSampleTimestamp"[5]')
            eI1time_stamp_last_sample_ns_node = ua_client.get_node(
                'ns=3;s="LEdgeBuffer_SwitchBuffer"."edgeInterface"[1]."dataBuffer"."header"."lastSampleTimestamp"[6]')

            traj_contains_flag_node = ua_client.get_node('ns=3;s="Buffer_data"."Data"."TrajectoryContainsFlags"')

            num_of_packets = 24

            # Data transfer
            # Step 0
            enable_switch_buffer_node.set_value(DataValue(Variant(False, VariantType.Boolean)))

            # Step 1
            signal_used_cell = [1] * num_of_traces
            for node, value in zip(lreal_signal_used_nodes, signal_used_cell):
                node.set_value(DataValue(Variant(value, VariantType.Boolean)))

            trace_selector_cell = [i for i in range(num_of_traces)]

            for node, value in zip(lreal_trace_selector_nodes, trace_selector_cell):
                node.set_value(DataValue(Variant(value, VariantType.Int16)))

            # Step 1.5
            val = eI0sample_nodes[0].get_data_value()
            val = val.Value.Value
            size_of_packet = len(val)
            samples = np.zeros((num_of_traces, size_of_packet * num_of_packets))
            time_first_and_last_matrix = np.zeros((14, num_of_packets))
            print(f"Size of packets: {size_of_packet}")

            # Step 2
            enable_switch_buffer_node.set_value(DataValue(Variant(True, VariantType.Boolean)))

            # Step 3
            val = [node.get_data_value() for node in trace_names_nodes]
            trace_names = [str(v.Value.Value) for v in val]
            rft = 0
            while rft == 0:
                ready_for_trigger = ready_for_trigger_node.get_data_value().Value.Value
                rft = ready_for_trigger

            # Step 3.5
            print("Waiting on flag")
            traj_contains_flag = 0
            while traj_contains_flag == 0:
                traj_contains_flag_read = traj_contains_flag_node.get_data_value().Value.Value
                traj_contains_flag = traj_contains_flag_read

            # Step 4
            start_recording_node.set_value(DataValue(Variant(True, VariantType.Boolean)))
            print("step 4")

            # Step 5 - loop to read samples in packages
            print("step 5")

            packet_no = 0
            while packet_no < num_of_packets:

                if packet_no % 2 == 0:  # edgeInterface[0]
                    hs_bit0 = 0
                    while hs_bit0 == 0:
                        #print("waiting for handshake bit if0")
                        hs_bit0_read = eI0handsake_bit_node.get_data_value().Value.Value
                        hs_bit0 = hs_bit0_read

                    val = [node.get_data_value() for node in eI0sample_nodes]

                    eI0handsake_bit_node.set_value(DataValue(Variant(False, VariantType.Boolean)))

                    for i in range(num_of_traces):
                        samples[i, packet_no * size_of_packet:(packet_no + 1) * size_of_packet] = val[i].Value.Value

                    val = [node.get_data_value() for node in
                           [eI0time_stamp_first_sample_year_node, eI0time_stamp_first_sample_month_node,
                            eI0time_stamp_first_sample_day_node, eI0time_stamp_first_sample_hours_node,
                            eI0time_stamp_first_sample_minutes_node, eI0time_stamp_first_sample_seconds_node,
                            eI0time_stamp_first_sample_ns_node, eI0time_stamp_last_sample_year_node,
                            eI0time_stamp_last_sample_month_node, eI0time_stamp_last_sample_day_node,
                            eI0time_stamp_last_sample_hours_node, eI0time_stamp_last_sample_minutes_node,
                            eI0time_stamp_last_sample_seconds_node, eI0time_stamp_last_sample_ns_node]]
                    for i in range(14):
                        time_first_and_last_matrix[i, packet_no] = val[i].Value.Value

                    if packet_no == 0:
                        first_sample_after_pretrigger_read = eI0first_sample_after_pretrigger_node.get_data_value().Value.Value
                        first_sample_after_pretrigger = float(first_sample_after_pretrigger_read)

                elif packet_no % 2 == 1:  # edgeInterface[1]
                    hs_bit1 = 0
                    while hs_bit1 == 0:
                        #print("waiting for handshake bit if1")
                        hs_bit1_read = eI1handsake_bit_node.get_data_value().Value.Value
                        hs_bit1 = hs_bit1_read
                    val = [node.get_data_value() for node in eI1sample_nodes]

                    eI1handsake_bit_node.set_value(DataValue(Variant(False, VariantType.Boolean)))

                    for i in range(num_of_traces):
                        samples[i, packet_no * size_of_packet:(packet_no + 1) * size_of_packet] = val[i].Value.Value

                    val = [node.get_data_value() for node in
                           [eI1time_stamp_first_sample_year_node, eI1time_stamp_first_sample_month_node,
                            eI1time_stamp_first_sample_day_node, eI1time_stamp_first_sample_hours_node,
                            eI1time_stamp_first_sample_minutes_node, eI1time_stamp_first_sample_seconds_node,
                            eI1time_stamp_first_sample_ns_node, eI1time_stamp_last_sample_year_node,
                            eI1time_stamp_last_sample_month_node, eI1time_stamp_last_sample_day_node,
                            eI1time_stamp_last_sample_hours_node, eI1time_stamp_last_sample_minutes_node,
                            eI1time_stamp_last_sample_seconds_node, eI1time_stamp_last_sample_ns_node]]
                    for i in range(14):
                        time_first_and_last_matrix[i, packet_no] = val[i].Value.Value

                else:
                    raise ValueError('Invalid index of edgeInterface')

                packet_no += 1

            enable_switch_buffer_node.set_value(DataValue(Variant(False, VariantType.Boolean)))
            # ua_client.disconnect()
            init_server = 0
            print('Transfer done. Postprocessing the data...')

            current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            np.save(f"samples{j}_{str(current_datetime)}.npy", samples)
            j += 1
            # transposed_array = samples.T
            # selected_cols = transposed_array[:, 4:10]

            selected_rows = samples[4:11, :]
            yield selected_rows
            print('Done')


if __name__ == "__main__":
    main()
