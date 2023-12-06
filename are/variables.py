from jitcdde import y

# instantiate jitcdde state variables
c_f1 = lambda tau=None: y(0, tau) if tau is not None else y(0)
c_f2 = lambda tau=None: y(1, tau) if tau is not None else y(1)
c_t1 = lambda tau=None: y(2, tau) if tau is not None else y(2)
c_c1 = lambda tau=None: y(3, tau) if tau is not None else y(3)
c_c2 = lambda tau=None: y(4, tau) if tau is not None else y(4)
c_m1 = lambda tau=None: y(5, tau) if tau is not None else y(5)
n = lambda tau=None: y(6, tau) if tau is not None else y(6)
C1 = lambda tau=None: y(7, tau) if tau is not None else y(7)
C2 = lambda tau=None: y(8, tau) if tau is not None else y(8)
C3 = lambda tau=None: y(9, tau) if tau is not None else y(9)
C4 = lambda tau=None: y(10, tau) if tau is not None else y(10)
C5 = lambda tau=None: y(11, tau) if tau is not None else y(11)
C6 = lambda tau=None: y(12, tau) if tau is not None else y(12)
rho = lambda tau=None: y(13, tau) if tau is not None else y(13)

hx_fh1_f1 = lambda tau=None: y(14, tau) if tau is not None else y(14)
hx_fh1_f2 = lambda tau=None: y(15, tau) if tau is not None else y(15)
hx_fh1_t1 = lambda tau=None: y(16, tau) if tau is not None else y(16)
hx_fh1_h1 = lambda tau=None: y(17, tau) if tau is not None else y(17)
hx_fh1_h2 = lambda tau=None: y(18, tau) if tau is not None else y(18)

hx_fh2_f1 = lambda tau=None: y(19, tau) if tau is not None else y(19)
hx_fh2_f2 = lambda tau=None: y(20, tau) if tau is not None else y(20)
hx_fh2_t1 = lambda tau=None: y(21, tau) if tau is not None else y(21)
hx_fh2_h1 = lambda tau=None: y(22, tau) if tau is not None else y(22)
hx_fh2_h2 = lambda tau=None: y(23, tau) if tau is not None else y(23)

hx_ch1_c1 = lambda tau=None: y(24, tau) if tau is not None else y(24)
hx_ch1_c2 = lambda tau=None: y(25, tau) if tau is not None else y(25)
hx_ch1_t1 = lambda tau=None: y(26, tau) if tau is not None else y(26)
hx_ch1_h1 = lambda tau=None: y(27, tau) if tau is not None else y(27)
hx_ch1_h2 = lambda tau=None: y(28, tau) if tau is not None else y(28)

hx_ch2_c1 = lambda tau=None: y(29, tau) if tau is not None else y(29)
hx_ch2_c2 = lambda tau=None: y(30, tau) if tau is not None else y(30)
hx_ch2_t1 = lambda tau=None: y(31, tau) if tau is not None else y(31)
hx_ch2_h1 = lambda tau=None: y(32, tau) if tau is not None else y(32)
hx_ch2_h2 = lambda tau=None: y(33, tau) if tau is not None else y(33)

hx_hwf1_h1 = lambda tau=None: y(34, tau) if tau is not None else y(34)
hx_hwf1_h2 = lambda tau=None: y(35, tau) if tau is not None else y(35)
hx_hwf1_t1 = lambda tau=None: y(36, tau) if tau is not None else y(36)
hx_hwf1_w1 = lambda tau=None: y(37, tau) if tau is not None else y(37)
hx_hwf1_w2 = lambda tau=None: y(38, tau) if tau is not None else y(38)

hx_hwf2_h1 = lambda tau=None: y(39, tau) if tau is not None else y(39)
hx_hwf2_h2 = lambda tau=None: y(40, tau) if tau is not None else y(40)
hx_hwf2_t1 = lambda tau=None: y(41, tau) if tau is not None else y(41)
hx_hwf2_w1 = lambda tau=None: y(42, tau) if tau is not None else y(42)
hx_hwf2_w2 = lambda tau=None: y(43, tau) if tau is not None else y(43)

hx_hwc1_h1 = lambda tau=None: y(44, tau) if tau is not None else y(44)
hx_hwc1_h2 = lambda tau=None: y(45, tau) if tau is not None else y(45)
hx_hwc1_t1 = lambda tau=None: y(46, tau) if tau is not None else y(46)
hx_hwc1_w1 = lambda tau=None: y(47, tau) if tau is not None else y(47)
hx_hwc1_w2 = lambda tau=None: y(48, tau) if tau is not None else y(48)

hx_hwc2_h1 = lambda tau=None: y(49, tau) if tau is not None else y(49)
hx_hwc2_h2 = lambda tau=None: y(50, tau) if tau is not None else y(50)
hx_hwc2_t1 = lambda tau=None: y(51, tau) if tau is not None else y(51)
hx_hwc2_w1 = lambda tau=None: y(52, tau) if tau is not None else y(52)
hx_hwc2_w2 = lambda tau=None: y(53, tau) if tau is not None else y(53)
