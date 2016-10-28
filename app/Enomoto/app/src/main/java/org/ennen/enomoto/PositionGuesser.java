package org.ennen.enomoto;

import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.location.LocationListener;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import java.io.IOException;
import java.util.List;
import java.util.Locale;
import java.util.Stack;

import static android.content.ContentValues.TAG;

/**
 * Created by asmateus on 28/10/16.
 */

public class PositionGuesser implements LocationListener
{
    public Stack stack;

    public PositionGuesser(Stack<String> stack)
    {
        this.stack = stack;
    }

    @Override
    public void onLocationChanged(Location loc)
    {
        stack.push("taskid=11&datetime=00-00-00_00:00:00&lon=" + loc.getLongitude() + "&lat=" + loc.getLatitude());
        Log.d("Lon", ""+loc.getLongitude());
        Log.d("lat", ""+loc.getLatitude());
    }

    @Override
    public void onProviderDisabled(String provider) {}

    @Override
    public void onProviderEnabled(String provider) {}

    @Override
    public void onStatusChanged(String provider, int status, Bundle extras) {}
}
