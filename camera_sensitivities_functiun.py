def eigen_decomposition(a, eigen_w_v_count=-1):
    A = np.dot(np.transpose(a), a)
    w, v = np.linalg.eigh(A)

    w = w[-eigen_w_v_count:]
    v = v[:, -eigen_w_v_count:]

    w = np.flipud(w)
    v = np.fliplr(v)

    return w, v
    
def PCA_Jiang2013(msds_camera_sensitivities, eigen_w_v_count=1):
    red_sensitivities, green_sensitivities, blue_sensitivities = [], [], []

    def normalised_sensitivity(msds, channel):
        return msds.signals[channel].copy().normalise().values

    for msds in msds_camera_sensitivities.values():
        red_sensitivities.append(normalised_sensitivity(msds, msds.labels[0]))
        green_sensitivities.append(normalised_sensitivity(msds, msds.labels[1]))
        blue_sensitivities.append(normalised_sensitivity(msds, msds.labels[2]))

    red_w_v = eigen_decomposition(
        np.vstack(red_sensitivities), eigen_w_v_count)
    green_w_v = eigen_decomposition(
        np.vstack(green_sensitivities), eigen_w_v_count)
    blue_w_v = eigen_decomposition(
        np.vstack(blue_sensitivities), eigen_w_v_count)

    return red_w_v, green_w_v, blue_w_v
    
def recover_camera_sensitivity(RGB, illuminant, reflectances, eigen_w_v,
                               shape):
    A = []

    for reflectance in reflectances:
        A.append(
            np.dot(
                np.dot(reflectance, np.diag(illuminant)),
                eigen_w_v[1]) * shape.interval)

    X = np.linalg.lstsq(A, RGB)[0]
    X = np.dot(eigen_w_v[1], X)

    return X
