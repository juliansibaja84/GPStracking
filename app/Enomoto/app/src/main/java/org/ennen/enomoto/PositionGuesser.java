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
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.List;
import java.util.Locale;
import java.util.Stack;

import static android.content.ContentValues.TAG;
import static java.lang.Math.abs;

/**
 * Created by asmateus on 28/10/16.
 */

public class PositionGuesser implements LocationListener
{
    public Stack stack;
    public double prev_lat = 0;
    public double prev_lon = 0;
    public long prev_tim = 0;
    public float speed = 0;
    public float dis = 0;
    public double rpm = 0;

    public PositionGuesser(Stack<String> stack)
    {
        this.stack = stack;
    }

    @Override
    public void onLocationChanged(Location loc)
    {
        DateFormat df = new SimpleDateFormat("dd-MM-yyyy_HH:mm:ss");
        Calendar c = Calendar.getInstance();
        stack.push("taskid=11&datetime="+df.format(c.getTime())+"&lon=" + loc.getLongitude() + "&lat=" + loc.getLatitude() + "&idT=2");
        Log.d("Lon", ""+loc.getLongitude());
        Log.d("lat", ""+loc.getLatitude());
        if(prev_lat != 0 && prev_lon != 0) {
            dis = distanceCalculator(prev_lat, prev_lon, loc.getLatitude(), loc.getLongitude());
            speed = 3600000*dis/abs(System.currentTimeMillis() - prev_tim);
            stack.push("taskid=" + 5 + "&datetime=" + df.format(c.getTime()) + "&val=" + speed + "&idT=2");
            Log.d("speed", "" + speed);
            rpm = (1000*speed/3600)/0.5291328;
            stack.push("taskid=" + 2 + "&datetime=" + df.format(c.getTime()) + "&val=" + rpm + "&idT=2");
            Log.d("rpm", "" + rpm);
        }
        else {
            prev_lon = loc.getLongitude();
            prev_lat = loc.getLatitude();
            prev_tim = System.currentTimeMillis();
        }
    }

    @Override
    public void onProviderDisabled(String provider) {}

    @Override
    public void onProviderEnabled(String provider) {}

    @Override
    public void onStatusChanged(String provider, int status, Bundle extras) {}

    public float distanceCalculator(double lat1, double lng1, double lat2, double lng2)
    {
        double earthRadius = 6371; //kilometers
        double dLat = Math.toRadians(lat2-lat1);
        double dLng = Math.toRadians(lng2-lng1);
        double a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2)) *
                        Math.sin(dLng/2) * Math.sin(dLng/2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        float dist = (float) (earthRadius * c);

        return dist;
    }
}
