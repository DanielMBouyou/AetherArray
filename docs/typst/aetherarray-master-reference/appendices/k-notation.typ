#import "../template.typ": *

== Appendix K. Notation

#table(
  columns: (1.0fr, 3.3fr, 1.8fr),
  table.header([Symbol], [Meaning], [Unit]),
  [$f$, $f_0$], [frequency; working frequency 2.44 GHz], [Hz],
  [$lambda_0$, $lambda_g$], [free space and guided wavelength], [m],
  [$k = 2 pi \/ lambda_0$, $beta$, $alpha$, $gamma$], [free space wavenumber; phase, attenuation and propagation constants], [rad/m, Np/m, 1/m],
  [$epsilon_r$, $epsilon_"eff"$, $tan delta$], [relative and effective permittivity; loss tangent], [dimensionless],
  [$h$, $W$, $t$], [substrate height, trace width, copper thickness], [m],
  [$Z_0$, $Z_L$, $Gamma$], [characteristic and load impedance; reflection coefficient], [ohm, ohm, dimensionless],
  [$a_i$, $b_i$, $S_(i j)$], [incident and outgoing waves; scattering parameters], [$sqrt("W")$, dimensionless],
  [$N$, $d$, $theta$, $theta_0$], [element count, spacing, observation and steering angles], [count, m, rad],
  [$A F ( theta )$], [array factor], [dimensionless],
  [$vb(a) ( theta )$], [steering vector], [dimensionless],
  [$vb(x)$, $vb(w)$], [commanded state; weights], [16 bit word; complex],
  [$vb(H)_t$, $h_n = g_n e^(j psi_n)$], [array state; per channel gain and phase], [complex],
  [$vb(z)_t$], [identifiable relative parameters, six at $N = 4$], [mixed: log ratio, rad],
  [$vb(S)_A$, $vb(S)_(B o)$, $vb(C)$], [antenna board scattering matrix; beamformer reverse path; coupling operator], [dimensionless],
  [$sigma_q$], [quantisation residual, 12.99 degrees], [deg],
  [$eta$, $eta_c$], [budget fractions], [dimensionless],
  [$T$], [phase agreement threshold, 2.29 degrees], [deg],
  [$U$], [analyser expanded uncertainty], [per S term],
  [$y_k$, $epsilon.alt_k$], [measurement and noise], [V or complex],
  [$cal(D)$], [history of sessions], [data],
  [$p_theta$], [learned prior], [probability density],
  [$M_"required"$], [new measurements needed to reach the target], [count],
  [$bb(I)$, $bb(H)$], [mutual information; entropy], [nats],
)
