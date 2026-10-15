package es.csic.mineralesestrategicos;

import android.webkit.WebSettings;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onStart() {
        super.onStart();
        if (getBridge() != null && getBridge().getWebView() != null) {
            WebSettings s = getBridge().getWebView().getSettings();
            // Que el tamaño de letra del sistema no agrande la web: la app usa siempre su propio tamaño.
            s.setTextZoom(100);
            // Zoom con dos dedos, sin los botones +/- en pantalla.
            s.setSupportZoom(true);
            s.setBuiltInZoomControls(true);
            s.setDisplayZoomControls(false);
        }
    }
}
