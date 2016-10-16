package org.ennen.enomoto;

import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.DialogInterface;
import android.content.Intent;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Set;

/**
 * Created by asmateus on 15/10/16.
 */

public class BluetoothConnector
{
    private static final int REQUEST_ENABLE_BT = 1;
    private ArrayList<String> paired_adapter_list = new ArrayList<>();
    private BluetoothAdapter mBlAdapter;
    private MainActivity master;

    public String selected_device_MAC = "";

    public BluetoothConnector(MainActivity master)
    {
        this.master = master;
        this.mBlAdapter = BluetoothAdapter.getDefaultAdapter();
        if (mBlAdapter == null) {
            Toast toast = Toast.makeText(master.getApplicationContext(), "Bluetooth not Supported", Toast.LENGTH_LONG);
            toast.show();
        }
        else {
            if (!this.mBlAdapter.isEnabled()) {
                Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                master.startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
            }
            else
                searchPairedDevices();
        }
    }

    public boolean blStatus()
    {
        return (this.mBlAdapter != null && this.mBlAdapter.getBondedDevices().size() > 0);
    }

    private void searchPairedDevices()
    {
        Set<BluetoothDevice> pairedDevices = this.mBlAdapter.getBondedDevices();
        // If there are paired devices
        if (pairedDevices.size() > 0) {
            // Loop through paired devices
            for (BluetoothDevice device : pairedDevices) {
                // Add the name and address to an array adapter to show in a ListView
                paired_adapter_list.add(device.getName() + "\n" + device.getAddress());
            }
            buildSelectDialog();
        }
        else {
            Toast toast = Toast.makeText(master.getApplicationContext(), "Please pair with your OBD-II Adapter and try again", Toast.LENGTH_LONG);
            toast.show();
        }
    }

    private void buildSelectDialog()
    {
        AlertDialog.Builder builder = new AlertDialog.Builder(master);
        builder.setTitle("Select Adapter");
        builder.setItems(
                this.paired_adapter_list.toArray(new CharSequence[this.paired_adapter_list.size()]),
                new DialogInterface.OnClickListener()
                {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        selected_device_MAC = paired_adapter_list.get(which).split("\n")[1];
                        Toast toast = Toast.makeText(master.getApplicationContext(), "Selected " + selected_device_MAC, Toast.LENGTH_LONG);
                        toast.show();
                    }
                });
        builder.show();
    }
}
